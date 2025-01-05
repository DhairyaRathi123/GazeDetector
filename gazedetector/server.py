from flask import Flask, jsonify, Response
from flask_cors import CORS
from .detector import GazeDetector
import cv2

app = Flask(__name__)
CORS(app)

detector = GazeDetector()

def gen_frames():
    while True:
        status, frame = detector.detect()
        if frame is None:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    status, _ = detector.detect()
    return jsonify(status=status)

def run_server():
    app.run(debug=True)
