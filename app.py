from flask import Flask, jsonify, request, render_template
import gaze_detection  # Import your gaze detection logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gaze', methods=['POST'])
def detect_gaze():
    file = request.files['image']
    result = gaze_detection.detect_gaze(file)
    return jsonify(result)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    answer = request.form.get('answer')
    # Process the answer (e.g., save to database or evaluate)
    return jsonify({'message': f'You selected answer: {answer}'})

if __name__ == "__main__":
    app.run(debug=True)
