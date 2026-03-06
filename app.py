from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import instaloader
import os
import glob

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "temp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return {"status": "API running"}

@app.route("/download", methods=["POST"])
def download():

    data = request.json
    url = data.get("url")

    loader = instaloader.Instaloader(
        dirname_pattern=DOWNLOAD_FOLDER,
        download_pictures=False
    )

    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    loader.download_post(post, target=DOWNLOAD_FOLDER)

    files = glob.glob(f"{DOWNLOAD_FOLDER}/*.mp4")

    if not files:
        return jsonify({"error": "Download failed"})

    return send_file(files[-1], as_attachment=True)