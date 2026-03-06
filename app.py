from flask import Flask, request, send_file, jsonify
import instaloader
import os
import glob
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "temp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_instagram_video(post_url):

    loader = instaloader.Instaloader(
        dirname_pattern=DOWNLOAD_FOLDER,
        download_pictures=False,
        download_video_thumbnails=False,
        save_metadata=False
    )

    shortcode = post_url.split("/")[-2]

    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    loader.download_post(post, target=DOWNLOAD_FOLDER)

    files = glob.glob(f"{DOWNLOAD_FOLDER}/*.mp4")

    if files:
        return files[-1]

    return None


@app.route("/download", methods=["POST"])
def download():

    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_path = download_instagram_video(url)

    if not video_path:
        return jsonify({"error": "Download failed"}), 500

    return send_file(video_path, as_attachment=True)


if __name__ == "__main__":
    app.run()