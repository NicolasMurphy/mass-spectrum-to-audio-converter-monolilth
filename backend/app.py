import os
from flask import Flask
from flask_cors import CORS
from db import init_pool
from api.routes import serve_frontend, history, generate_audio_with_data, popular

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

app.route("/")(serve_frontend)
app.route("/history", methods=["GET"])(history)
app.route("/massbank/<algorithm>", methods=["POST"])(generate_audio_with_data)
app.route("/popular", methods=["GET"])(popular)

if __name__ == "__main__":
    app.run(debug=True)
