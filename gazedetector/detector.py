import cv2

class GazeDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)

    def detect(self):
        success, frame = self.cap.read()
        if not success:
            return "Error: Cannot access camera", None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return "in sight" if len(faces) > 0 else "out of sight", frame

    def release(self):
        self.cap.release()
