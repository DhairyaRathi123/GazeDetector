from flask import Flask, request, jsonify, send_from_directory
import base64
from io import BytesIO
import cv2
import numpy as np
import mediapipe as mp
import os

app = Flask(__name__)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

# Serve the index.html from the static folder
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/process-frame', methods=['POST'])
def process_frame():
    # Get the base64 image from the request
    data = request.get_json()
    img_data = data['frame'].split(',')[1]
    img_bytes = base64.b64decode(img_data)

    # Convert the image bytes to a NumPy array
    np_array = np.frombuffer(img_bytes, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Convert the frame to RGB (MediaPipe works with RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    # Check if a face is detected
    if results.detections:
        status = "in sight"
    else:
        status = "out of sight"

    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(debug=True)
