import base64, os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from audio import generate_combined_wav_bytes_and_data
from db import (
    get_massbank_peaks,
    log_search,
    get_search_history,
    get_popular_compounds,
    init_pool,
)
from utils.rate_limiting import is_rate_limited
from utils.webhook import send_webhook_notification
from api.validation import validate_algorithm, validate_and_parse_parameters
import threading

init_pool()


app = Flask(__name__)
CORS(
    app,
    origins=os.getenv(
        "CORS_ORIGINS",
        "https://mass-spectrum-to-audio-converter.vercel.app",  # fallback
    ).split(","),
    expose_headers=["X-Compound", "X-Accession"],
)


@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")


@app.route("/history", methods=["GET"])
def history():
    try:
        limit = request.args.get("limit", default=20, type=int)
        history_data = get_search_history(limit=limit)
        return {"history": history_data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/massbank/<algorithm>", methods=["POST"])
def generate_audio_with_data(algorithm):
    ip = (
        request.headers.get("X-Forwarded-For", request.remote_addr or "")
        .split(",")[0]
        .strip()
    )
    if is_rate_limited(ip):
        return {"error": "Rate limit exceeded. Try again later."}, 429

    try:
        validate_algorithm(algorithm)
    except ValueError as e:
        return {"error": str(e)}, 400

    data = request.get_json()

    try:
        params = validate_and_parse_parameters(data)
    except ValueError as e:
        return {"error": str(e)}, 400

    try:
        spectrum, accession, compound_actual = get_massbank_peaks(params["compound"])

        wav_buffer, transformed_data = generate_combined_wav_bytes_and_data(
            spectrum,
            offset=params["offset"],
            scale=params["scale"],
            shift=params["shift"],
            duration=params["duration"],
            sample_rate=params["sample_rate"],
            algorithm=algorithm,
            factor=params["factor"],
            modulus=params["modulus"],
            base=params["base"],
        )

        # log AFTER audio generation
        threading.Thread(
            target=log_search, args=(compound_actual, accession), daemon=True
        ).start()

        # send webhook AFTER audio generation (background thread)
        def send_webhook_async():
            send_webhook_notification(
                compound_actual,
                accession,
                algorithm,
                params["duration"],
                params["sample_rate"],
            )

        threading.Thread(target=send_webhook_async, daemon=True).start()

        audio_base64 = base64.b64encode(wav_buffer.getvalue()).decode()

        # Prepare algorithm parameters based on algorithm type
        if algorithm == "linear":
            algorithm_params = {"offset": params["offset"]}
        elif algorithm == "inverse":
            algorithm_params = {"scale": params["scale"], "shift": params["shift"]}
        elif algorithm == "modulo":
            algorithm_params = {
                "factor": params["factor"],
                "modulus": params["modulus"],
                "base": params["base"],
            }

        # Build response
        response_data = {
            "compound": compound_actual,
            "accession": accession,
            "audio_base64": audio_base64,
            "spectrum": transformed_data,
            "algorithm": algorithm,
            "parameters": algorithm_params,
            "audio_settings": {
                "duration": params["duration"],
                "sample_rate": params["sample_rate"],
            },
        }

        return response_data, 200

    except ValueError as e:
        error_msg = str(e)
        if "No records found" in error_msg:
            return {"error": error_msg}, 404
        else:
            return {"error": error_msg}, 400
    except Exception as e:
        return {"error": "Internal server error"}, 500


@app.route("/popular", methods=["GET"])
def popular():
    try:
        limit = request.args.get("limit", default=20, type=int)
        popular_data = get_popular_compounds(limit=limit)
        return {"popular": popular_data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)
