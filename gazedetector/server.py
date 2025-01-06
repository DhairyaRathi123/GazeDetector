from flask import Flask, jsonify, Response, send_from_directory
from flask_cors import CORS
from .detector import GazeDetector
import cv2
import os

app = Flask(__name__)
CORS(app)

detector = None

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

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'index.html')

@app.route('/toggle_camera', methods=['POST'])
def toggle_camera():
    global detector
    if detector is not None:
        detector.release()
        detector = None
        return jsonify(status="Camera turned off")
    else:
        detector = GazeDetector()
        return jsonify(status="Camera turned on")

def run_server(show_screen=True, realtime=True, htmlembedd=False):
    global detector
    detector = GazeDetector()

    if show_screen:
        while True:
            status, frame = detector.detect()
            if frame is not None:
                cv2.imshow('Gaze Detector', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        detector.release()
        cv2.destroyAllWindows()
    elif htmlembedd:
        app.run(debug=True)
    else:
        while True:
            status, _ = detector.detect()
            print(status)
