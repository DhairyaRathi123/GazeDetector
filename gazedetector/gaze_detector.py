"""
MIT License

Copyright (c) [2025] [D_LABS]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Gazedetector"), to deal
in the GazeDetector without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the GazeDetector, and to permit persons to whom the GazeDetector is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the GazeDetector.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import shutil
from flask import Flask, send_from_directory, jsonify, request
import base64
import cv2
import numpy as np
import mediapipe as mp

# Initialize Flask app
app = Flask(__name__)

# Path to the static files directory
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Ensure static folder is created and index.html is there
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

# Ensure index.html is present in the static folder
if not os.path.exists(os.path.join(static_folder, 'index.html')):
    from pkg_resources import resource_filename
    index_html_path = resource_filename(__name__, 'static/index.html')
    shutil.copy(index_html_path, os.path.join(static_folder, 'index.html'))

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

# Serve the index.html from the static folder
@app.route('/')
def index():
    return send_from_directory(static_folder, 'index.html')

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

# Function to run the Flask server
def run_server():
    app.run(debug=True)
