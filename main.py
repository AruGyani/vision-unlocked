import cv2

def detect_pupil(eye_roi):

def draw_gaze_direction(frame, eye_position, pupil_center, eye_size):

# Initialize the camera
cap = cv2.VideoCapture(0)

# Load Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Variables for blink detection
prev_pupil_radius = None
blink_counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

    for (ex, ey, ew, eh) in eyes:
        eye_roi = gray[ey:ey + eh, ex:ex + ew]
        pupil_center, pupil_radius = detect_pupil(eye_roi)

        if pupil_center and pupil_radius:
            cv2.circle(frame, (ex + pupil_center[0], ey + pupil_center[1]), pupil_radius, (255, 0, 0), 2)
            draw_gaze_direction(frame, (ex, ey), pupil_center, (ew, eh))

            # Blink detection
            if prev_pupil_radius is not None:
                # Compare current and previous pupil sizes
                size_difference = abs(pupil_radius - prev_pupil_radius)

                # If a significant change in size is detected, consider it a blink
                if size_difference > 3:
                    blink_counter += 1
                    print("Blink detected! Count:", blink_counter)

            # Update previous pupil radius
            prev_pupil_radius = pupil_radius

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
