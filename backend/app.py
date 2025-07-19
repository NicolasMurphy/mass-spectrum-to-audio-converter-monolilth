import time, base64
from flask import Flask, request, send_file, send_from_directory
from converter import generate_combined_wav_bytes, generate_combined_wav_bytes_and_data
from massbank import get_massbank_peaks
from flask_cors import CORS
from db.queries import log_search
from db.queries import get_search_history


RATE_LIMIT = 10
WINDOW = 60
ip_buckets = {}


def is_rate_limited(ip):
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
    origins=[
        "http://localhost:5173",
        "https://mass-spectrum-to-audio-converter.vercel.app",
    ],
    expose_headers=["X-Compound", "X-Accession"],
)


@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")


@app.route("/massbank/<algorithm>", methods=["GET"])
def generate_audio(algorithm):

    ip = (
        request.headers.get("X-Forwarded-For", request.remote_addr or "")
        .split(",")[0]
        .strip()
    )
    print(f"Client IP: {ip}")
    if is_rate_limited(ip):
        return {"error": "Rate limit exceeded. Try again later."}, 429

    if algorithm not in ["linear", "inverse"]:
        return {"error": f"Unsupported algorithm '{algorithm}'"}, 400
    compound = request.args.get("compound")
    offset = request.args.get("offset", type=float, default=300)
    # logShift = request.args.get("logShift", type=float, default=1)
    # scale = request.args.get("scale", type=float, default=300)
    scale = request.args.get("scale", type=float, default=100000)
    shift = request.args.get("shift", type=float, default=1)
    sample_rate = request.args.get("sample_rate", type=int, default=96000)
    duration = request.args.get("duration", type=float, default=5.0)

    if not compound:
        return {"error": "No compound provided"}, 400

    if not (0.01 <= duration <= 30):
        return {"error": "Duration must be between 0.01 and 30 seconds."}, 400

    if not 3500 <= sample_rate <= 192000:
        return {"error": "Sample rate must be between 3500 and 192000"}, 400

    raw_sr = request.args.get("sample_rate")
    if raw_sr is not None:  # Only validate if parameter was provided
        try:
            sample_rate = int(raw_sr)
        except (ValueError, TypeError):
            return {"error": "Invalid sample rate. Must be an integer."}, 400

    try:
        spectrum, accession, compound_actual = get_massbank_peaks(compound)

        log_search(compound_actual, accession)

        # see before and after values
        # print("\n=== Original Spectrum ===")
        # for mz, intensity in spectrum:
        #     print(f"m/z: {mz:.2f}, intensity: {intensity:.2f}")

        # print("\n=== Adjusted Spectrum ===")
        # for mz, intensity in spectrum:
        #     freq = mz + offset
        #     print(f"freq: {freq:.2f}, intensity: {intensity:.2f}")

        wav_buffer = generate_combined_wav_bytes(
            spectrum,
            offset=offset,
            # logShift=logShift,
            # scale=scale,
            scale=scale,
            shift=shift,
            duration=duration,
            sample_rate=sample_rate,
            algorithm=algorithm,
        )
        response = send_file(
            wav_buffer,
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f"{compound_actual}-{accession}.wav",
        )
        response.headers["X-Compound"] = compound_actual
        response.headers["X-Accession"] = accession
        return response

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/history", methods=["GET"])
def history():
    try:
        limit = request.args.get("limit", default=10, type=int)
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
    print(f"Client IP: {ip}")
    if is_rate_limited(ip):
        return {"error": "Rate limit exceeded. Try again later."}, 429

    if algorithm not in ["linear", "inverse"]:
        return {"error": f"Unsupported algorithm '{algorithm}'"}, 400

    # Get JSON data from request body
    data = request.get_json()
    if not data:
        return {"error": "No JSON data provided"}, 400

    compound = data.get("compound")
    offset = float(data.get("offset", 300))
    scale = float(data.get("scale", 100000))
    shift = float(data.get("shift", 1))
    sample_rate = int(data.get("sample_rate", 96000))
    duration = float(data.get("duration", 5.0))

    if not compound:
        return {"error": "No compound provided"}, 400

    if not (0.01 <= duration <= 30):
        return {"error": "Duration must be between 0.01 and 30 seconds."}, 400

    if not 3500 <= sample_rate <= 192000:
        return {"error": "Sample rate must be between 3500 and 192000"}, 400

    # Validate sample_rate is integer
    if not isinstance(sample_rate, int):
        return {"error": "Invalid sample rate. Must be an integer."}, 400

    try:
        spectrum, accession, compound_actual = get_massbank_peaks(compound)

        log_search(compound_actual, accession)

        wav_buffer, transformed_data = generate_combined_wav_bytes_and_data(
            spectrum,
            offset=offset,
            scale=scale,
            shift=shift,
            duration=duration,
            sample_rate=sample_rate,
            algorithm=algorithm,
        )

        audio_base64 = base64.b64encode(wav_buffer.getvalue()).decode()

        # Prepare algorithm parameters based on algorithm type
        if algorithm == "linear":
            algorithm_params = {"offset": offset}
        elif algorithm == "inverse":
            algorithm_params = {"scale": scale, "shift": shift}

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

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)
