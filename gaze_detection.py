import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def detect_gaze(image_file):
    # Convert file to a format suitable for OpenCV
    image = np.frombuffer(image_file.read(), np.uint8)
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # Initialize MediaPipe FaceMesh
    with mp_face_mesh.FaceMesh(max_num_faces=1) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Define the screen boundaries
        screen_boundaries = {'left': 0.2, 'right': 0.8, 'top': 0.2, 'bottom': 0.8}
        
        gaze_data = {'gaze_direction': 'unknown', 'alert': False}
        
        if results.multi_face_landmarks:
            # For simplicity, assume we have one face and use its landmarks
            landmarks = results.multi_face_landmarks[0]
            # Get the coordinates of the eyes (or other relevant landmarks)
            eye_landmarks = [landmarks.landmark[i] for i in [33, 133]]  # Example indices for eyes
            
            # Convert normalized coordinates to pixel coordinates
            h, w, _ = frame.shape
            eye_x = int(eye_landmarks[0].x * w)
            eye_y = int(eye_landmarks[0].y * h)
            
            # Check if gaze is within screen boundaries
            if (screen_boundaries['left'] * w < eye_x < screen_boundaries['right'] * w and
                screen_boundaries['top'] * h < eye_y < screen_boundaries['bottom'] * h):
                gaze_data['gaze_direction'] = 'within screen'
                gaze_data['alert'] = False
            else:
                gaze_data['gaze_direction'] = 'out of screen'
                gaze_data['alert'] = True

    return gaze_data
