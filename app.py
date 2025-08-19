import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from db import init_pool
from api.routes import history, generate_audio_with_data, popular

init_pool()

app = Flask(__name__, static_folder="static", static_url_path="")

# Update CORS for monolith - no longer need external origins
CORS(
    app,
    origins=["http://localhost:5000", "http://127.0.0.1:5000"],  # Local development
    expose_headers=["X-Compound", "X-Accession"],
)


# Serve React app for root and any non-API routes
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/<path:path>")
def serve_static_or_spa(path):
    # API routes - let Flask handle these normally
    if (
        path.startswith("api/")
        or path in ["history", "popular"]
        or path.startswith("massbank/")
    ):
        # These will be handled by the route decorators below
        return app.send_static_file(path)

    # Try to serve static file first
    try:
        return send_from_directory("static", path)
    except FileNotFoundError:
        # For React Router - serve index.html for unknown routes
        return send_from_directory("static", "index.html")


# API Routes (keeping your existing structure)
app.route("/history", methods=["GET"])(history)
app.route("/massbank/<algorithm>", methods=["POST"])(generate_audio_with_data)
app.route("/popular", methods=["GET"])(popular)

if __name__ == "__main__":
    # Important: bind to 0.0.0.0 for Docker, not 127.0.0.1
    app.run(host="0.0.0.0", port=5000, debug=True)
