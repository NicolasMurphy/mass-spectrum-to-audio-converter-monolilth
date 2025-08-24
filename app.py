from flask import Flask, send_from_directory
from flask_cors import CORS
from db import init_pool
from api.routes import history, generate_audio_with_data, popular

init_pool()

app = Flask(__name__, static_folder="static", static_url_path="")

CORS(
    app,
    expose_headers=["X-Compound", "X-Accession"],
)


@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/<path:path>")
def serve_static_or_spa(path):
    if (
        path.startswith("api/")
        or path in ["history", "popular"]
        or path.startswith("massbank/")
    ):
        return app.send_static_file(path)

    try:
        return send_from_directory("static", path)
    except FileNotFoundError:
        return send_from_directory("static", "index.html")


app.route("/history", methods=["GET"])(history)
app.route("/massbank/<algorithm>", methods=["POST"])(generate_audio_with_data)
app.route("/popular", methods=["GET"])(popular)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
