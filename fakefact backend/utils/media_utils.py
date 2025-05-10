from PIL import Image
import io
import base64
import cv2

def encode_image_from_path(filepath):
    image = Image.open(filepath)
    image.thumbnail((1024, 1024))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8'), "image/jpeg"

def extract_frame_base64(filepath):
    cap = cv2.VideoCapture(filepath)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None, "Unable to extract frame"
    is_success, buffer = cv2.imencode(".jpg", frame)
    if not is_success:
        return None, "Failed to encode frame"
    encoded_img = base64.b64encode(buffer).decode('utf-8')
    return encoded_img, "image/jpeg"
