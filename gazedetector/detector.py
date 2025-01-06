import cv2
import time

class GazeDetector:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.last_capture_time = 0

    def release(self):
        self.camera.release()

    def detect(self):
        current_time = time.time()
        if current_time - self.last_capture_time >= 1:  # Capture photo every second
            self.last_capture_time = current_time
            ret, frame = self.camera.read()
            if ret:
                return "in sight", frame  # Simplified for demonstration
            else:
                return "out of sight", None
        return "waiting", None
