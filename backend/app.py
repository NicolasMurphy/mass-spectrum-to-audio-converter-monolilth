from flask import Flask, request, send_file, send_from_directory
from converter import generate_combined_wav_bytes
from massbank import get_massbank_peaks
from flask_cors import CORS

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


@app.route("/massbank/linear", methods=["GET"])
def generate_audio():
    compound = request.args.get("compound")
    offset = request.args.get("offset", type=float, default=300)
    sample_rate = request.args.get("sample_rate", type=int, default=96000)
    duration = request.args.get("duration", type=float, default=5.0)

    if not compound:
        return {"error": "No compound provided"}, 400

    if not (0.01 <= duration <= 30):
        return {"error": "Duration must be between 0.01 and 30 seconds."}, 400

    if not 3500 <= sample_rate <= 192000:
        return {"error": "Sample rate must be between 3500 and 192000"}, 400

    raw_sr = request.args.get("sample_rate")
    try:
        sample_rate = int(raw_sr)
    except (ValueError, TypeError):
        return {"error": "Invalid sample rate. Must be an integer."}, 400

    try:
        spectrum, accession, compound_actual = get_massbank_peaks(compound)

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
            duration=duration,
            sample_rate=sample_rate,
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


if __name__ == "__main__":
    app.run(debug=True)
