from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime
import sys

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))
from ai.recommendation import get_recommendation

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def home():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/style.css")
def style():
    return send_from_directory(FRONTEND, "style.css")


@app.get("/script.js")
def script():
    return send_from_directory(FRONTEND, "script.js")


@app.get("/api/health")
def health():
    return jsonify({"success": True, "message": "StyleAI recommendation server is running"})


@app.post("/api/recommend")
def recommend():
    occasion = (request.form.get("occasion") or "").strip()
    outfit_type = (request.form.get("outfitType") or "").strip()
    color = (request.form.get("color") or "").strip()
    image = request.files.get("image")

    missing = []
    if not occasion:
        missing.append("occasion")
    if not outfit_type:
        missing.append("outfit type")
    if not color:
        missing.append("preferred color")
    if missing:
        return jsonify({"success": False, "error": "Please select: " + ", ".join(missing) + "."}), 400

    if image is None or not image.filename:
        return jsonify({"success": False, "error": "Please upload your photo."}), 400

    if not allowed_file(image.filename):
        return jsonify({"success": False, "error": "Use PNG, JPG, JPEG or WEBP (maximum 10 MB)."}), 400

    original = secure_filename(image.filename)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{stamp}_{original}"
    saved_path = UPLOADS / filename
    image.save(saved_path)

    recommendation = get_recommendation(
        occasion=occasion,
        outfit_type=outfit_type,
        color=color,
        image_path=str(saved_path),
    )

    return jsonify({
        "success": True,
        "recommendation": recommendation,
        "imageUrl": f"/uploads/{filename}",
    })


@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOADS, filename)


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"success": False, "error": "Image is too large. Maximum size is 10 MB."}), 413


if __name__ == "__main__":
    print("\nStyleAI is running at http://127.0.0.1:5000")
    print("Open that address in your browser. Press CTRL+C to stop.\n")
    app.run(host="127.0.0.1", port=5000, debug=True)

