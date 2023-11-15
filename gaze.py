import cv2
import dlib
import numpy as np

up_threshold = 0
down_threshold = 0.25
# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def analyze_gaze(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        left_eye = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)])
        right_eye = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)])

        left_EAR = get_eye_aspect_ratio(left_eye)
        right_EAR = get_eye_aspect_ratio(right_eye)

        if left_EAR < up_threshold and right_EAR < up_threshold:
            return "Looking Up"
        elif left_EAR > down_threshold and right_EAR > down_threshold:
            return "Looking Down"
    
    return "Gaze Direction Unknown"

# Start the webcam feed
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gaze_direction = analyze_gaze(frame)
    cv2.putText(frame, gaze_direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gaze Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
