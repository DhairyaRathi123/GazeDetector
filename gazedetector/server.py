from flask import Flask, jsonify, Response, send_from_directory, request
from flask_cors import CORS
from detector import GazeDetector
import os

app = Flask(__name__)
CORS(app)

detector = GazeDetector()

@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            status, frame = detector.detect()
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    if detector:
        detector.release()
        detector = None
        return jsonify(status="Camera turned off")
    else:
        detector = GazeDetector()
        return jsonify(status="Camera turned on")

def run_server(toggle_button=True, paste_in_html="index.html", pos={"w": "200px", "h": "100px"}, alignment="mid"):
    global detector

    # Save user HTML file to static directory if provided
    if paste_in_html:
        html_file = os.path.join(os.path.dirname(__file__), 'static', paste_in_html)
        if not os.path.exists(html_file):
            raise FileNotFoundError(f"The specified HTML file '{paste_in_html}' does not exist.")
        
    # Add positional styling for facecam
    facecam_style = f"position: fixed; top: 10px; right: 10px; width: {pos['w']}; height: {pos['h']};"
    if alignment == "mid":
        facecam_style = f"position: fixed; top: 10px; right: 50%; transform: translateX(50%); width: {pos['w']}; height: {pos['h']};"

    # Save the customized index.html content with positional styling
    with open(html_file, 'r') as file:
        content = file.read()
    content = content.replace('<img src="http://127.0.0.1:5000/video_feed" id="facecam">', f'<img src="http://127.0.0.1:5000/video_feed" id="facecam" style="{facecam_style}">')
    with open(html_file, 'w') as file:
        file.write(content)

    app.run(debug=True, port=5000)
