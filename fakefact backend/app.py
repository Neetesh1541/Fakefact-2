from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.ai_utils import auto_correct_text, ai_call, ai_image_check
from utils.media_utils import encode_image_from_path, extract_frame_base64
import os

app = Flask(__name__)
CORS(app)

@app.route("/check-sms", methods=["POST"])
def check_sms():
    sms = request.json.get("text", "")
    fixed = auto_correct_text(sms)
    prompt = f"Check this SMS for phishing or spam:\n{fixed}\nReply Safe / Suspicious with a short reason."
    return jsonify(ai_call(prompt))

@app.route("/check-news", methods=["POST"])
def check_news():
    news = request.json.get("text", "")
    fixed = auto_correct_text(news)
    prompt = f"Fact check this news:\n{fixed}\nReply with Likely True / Likely Fake and a percentage. Give a short reason."
    return jsonify(ai_call(prompt))

@app.route("/check-email", methods=["POST"])
def check_email():
    email = request.json.get("email", "")
    prompt = f"Check if this email '{email}' is suspicious. Answer Safe / Suspicious with reason."
    return jsonify(ai_call(prompt))

@app.route("/check-url", methods=["POST"])
def check_url():
    url = request.json.get("url", "")
    prompt = f"Check if the URL '{url}' is safe or phishing. Answer Safe / Unsafe with reason."
    return jsonify(ai_call(prompt))

@app.route("/check-image", methods=["POST"])
def check_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    filepath = "temp_image.jpg"
    file.save(filepath)
    encoded_img, mime_type = encode_image_from_path(filepath)
    os.remove(filepath)
    return jsonify(ai_image_check("Detect if this image is Real or Deepfake.", mime_type, encoded_img))

@app.route("/check-video", methods=["POST"])
def check_video():
    file = request.files.get("video")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    filepath = "temp_video.mp4"
    file.save(filepath)
    encoded_img, mime_type = extract_frame_base64(filepath)
    os.remove(filepath)
    if not encoded_img:
        return jsonify({"error": mime_type}), 500
    return jsonify(ai_image_check("Detect if this frame from video is Real or Deepfake.", mime_type, encoded_img))

@app.route("/chatbot", methods=["POST"])
def chatbot():
    question = request.json.get("question", "")
    fixed = auto_correct_text(question)
    prompt = f"Answer briefly:\n{fixed}"
    return jsonify(ai_call(prompt))

if __name__ == "__main__":
    app.run(debug=True)
