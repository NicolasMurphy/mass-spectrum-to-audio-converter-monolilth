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
        spectrum, accession, compound_actual = get_massbank_peaks(compound)
        wav_buffer = generate_combined_wav_bytes(spectrum)
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
