import time, base64, os
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
import requests
import threading

init_pool()

RATE_LIMIT = 20
WINDOW = 300
ip_buckets = {}


def cleanup_old_buckets():
    now = time.time()
    expired_ips = []

    for ip, timestamps in ip_buckets.items():
        recent_timestamps = [t for t in timestamps if now - t < WINDOW]

        if recent_timestamps:
            ip_buckets[ip] = recent_timestamps
        else:
            expired_ips.append(ip)

    for ip in expired_ips:
        del ip_buckets[ip]


def is_rate_limited(ip):
    cleanup_old_buckets()
    now = time.time()
    if ip not in ip_buckets:
        ip_buckets[ip] = []
    ip_buckets[ip] = [t for t in ip_buckets[ip] if now - t < WINDOW]
    if len(ip_buckets[ip]) >= RATE_LIMIT:
        return True
    ip_buckets[ip].append(now)
    return False


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

    if algorithm not in ["linear", "inverse", "modulo"]:
        return {
            "error": f"Unsupported algorithm: '{algorithm}'. Must be 'linear', 'inverse', or 'modulo'"
        }, 400

    # Get JSON data from request body
    data = request.get_json()
    if not data:
        return {"error": "No JSON data provided"}, 400

    # Validate sample_rate BEFORE conversion
    raw_sr = data.get("sample_rate")
    if raw_sr is not None:
        if isinstance(raw_sr, float) or (isinstance(raw_sr, str) and "." in raw_sr):
            return {"error": "Invalid sample rate. Must be an integer."}, 400

    compound = data.get("compound")
    try:
        offset = float(data.get("offset", 300))
    except (ValueError, TypeError):
        return {"error": "Invalid offset. Must be a float."}, 400
    try:
        scale = float(data.get("scale", 100000))
    except (ValueError, TypeError):
        return {"error": "Invalid scale. Must be a float."}, 400
    try:
        shift = float(data.get("shift", 1))
    except (ValueError, TypeError):
        return {"error": "Invalid shift. Must be a float."}, 400
    try:
        duration = float(data.get("duration", 5))
    except (ValueError, TypeError):
        return {"error": "Invalid duration. Must be a float."}, 400
    try:
        sample_rate = int(data.get("sample_rate", 44100))
    except (ValueError, TypeError):
        return {"error": "Invalid sample_rate. Must be an integer."}, 400
    try:
        factor = float(data.get("factor", 10))
    except (ValueError, TypeError):
        return {"error": "Invalid factor. Must be a float."}, 400
    try:
        modulus = float(data.get("modulus", 500))
    except (ValueError, TypeError):
        return {"error": "Invalid modulus. Must be a float."}, 400
    try:
        base = float(data.get("base", 100))
    except (ValueError, TypeError):
        return {"error": "Invalid base. Must be a float."}, 400

    if not compound or not compound.strip():
        return {"error": "No compound provided"}, 400

    if not (0.01 <= duration <= 30):
        return {"error": "Duration must be between 0.01 and 30 seconds."}, 400

    if not 3500 <= sample_rate <= 192000:
        return {"error": "Sample rate must be between 3500 and 192000"}, 400

    try:
        spectrum, accession, compound_actual = get_massbank_peaks(compound)

        wav_buffer, transformed_data = generate_combined_wav_bytes_and_data(
            spectrum,
            offset=offset,
            scale=scale,
            shift=shift,
            duration=duration,
            sample_rate=sample_rate,
            algorithm=algorithm,
            factor=factor,
            modulus=modulus,
            base=base,
        )

        # log AFTER audio generation
        threading.Thread(
            target=log_search, args=(compound_actual, accession), daemon=True
        ).start()

        # send webhook AFTER audio generation (background thread)
        def send_webhook_async():
            send_webhook_notification(
                compound_actual, accession, algorithm, duration, sample_rate
            )

        threading.Thread(target=send_webhook_async, daemon=True).start()

        audio_base64 = base64.b64encode(wav_buffer.getvalue()).decode()

        # Prepare algorithm parameters based on algorithm type
        if algorithm == "linear":
            algorithm_params = {"offset": offset}
        elif algorithm == "inverse":
            algorithm_params = {"scale": scale, "shift": shift}
        elif algorithm == "modulo":
            algorithm_params = {
                "factor": factor,
                "modulus": modulus,
                "base": base,
            }

        # Build response
        response_data = {
            "compound": compound_actual,
            "accession": accession,
            "audio_base64": audio_base64,
            "spectrum": transformed_data,
            "algorithm": algorithm,
            "parameters": algorithm_params,
            "audio_settings": {"duration": duration, "sample_rate": sample_rate},
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


def send_webhook_notification(
    compound_name, accession, algorithm, duration, sample_rate
):
    """Send webhook notification when a compound is generated"""
    webhook_url = os.getenv("WEBHOOK_URL")

    if not webhook_url:
        return

    payload = {
        "content": f"**New Compound Generated!**\n\n**Compound:** {compound_name}\n**Accession:** {accession}\n**Algorithm:** {algorithm}\n**Duration:** {duration}s\n**Sample Rate:** {sample_rate}Hz"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code == 204:
            print("Webhook sent successfully!")
        else:
            print(f"Webhook failed with status {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Webhook request failed: {e}")


if __name__ == "__main__":
    app.run(debug=True)
