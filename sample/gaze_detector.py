import cv2
import numpy as np


def get_eyes(eyes, frame_shape):
    if len(eyes) > 2:
        eyes = sorted(eyes, key=lambda e: e[2] * e[3], reverse=True)  # Sort by size
        for i in range(len(eyes)):
            for j in range(i + 1, len(eyes)):
                # Check if horizontally aligned and near the center of the frame
                if abs(eyes[i][1] - eyes[j][1]) < 20 and abs((eyes[i][0] + eyes[j][0]) / 2 - frame_shape[1] / 2) < frame_shape[1] / 4:
                    return [eyes[i], eyes[j]]
    return eyes[:2]


def detect_pupil(eye_roi):
    # Convert to grayscale and apply Gaussian blur
    blurred = cv2.GaussianBlur(eye_roi, (7, 7), 0)

    # Apply adaptive thresholding
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and circularity
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if area > 30 and circularity > 0.2:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            return (int(x), int(y)), int(radius)
    return None, None

def gaze_detector(frame, eye_position, pupil_center, eye_size):
    # Check if the pupil is in the upper or lower half of the eye
    eye_center_y = eye_position[1] + eye_size[1] // 2
    pupil_global_y = eye_position[1] + pupil_center[1]

    if pupil_global_y < eye_center_y:
        gaze_direction = "Up"
    else:
        gaze_direction = "Down"

    # Draw the direction on the frame
    cv2.putText(frame, gaze_direction, (eye_position[0], eye_position[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    