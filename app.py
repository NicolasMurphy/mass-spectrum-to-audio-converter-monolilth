from flask import Flask, request, send_file, send_from_directory
from converter import generate_combined_wav_bytes
from massbank import get_massbank_peaks

app = Flask(__name__)


@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")


@app.route("/generate", methods=["GET"])
def generate_audio():
    compound = request.args.get("compound")
    if not compound:
        return {"error": "No compound provided"}, 400

    try:
        spectrum = get_massbank_peaks(compound)
        wav_buffer = generate_combined_wav_bytes(spectrum)
        return send_file(
            wav_buffer,
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f"{compound}.wav",
        )
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)
