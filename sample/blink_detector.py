from imutils import face_utils
from face_utils import landmarks_to_np, eye_aspect_ratio
from collections import deque
import dlib
import numpy as np

print("[STATUS] Loading facial landmark predictor.")
predictor = dlib.shape_predictor('data/face_landmarks.dat')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

def blink_detector(img, rect, aspect_ratio_min=0.3, frame_consec_limit=3, counter=0, total=0):
  shape = predictor(img, rect)
  shape = landmarks_to_np(shape)

  leftEye = shape[lStart:lEnd]
  rightEye = shape[rStart:rEnd]

  leftEAR = eye_aspect_ratio(leftEye)
  rightEAR = eye_aspect_ratio(rightEye)

  ear = (leftEAR + rightEAR) / 2.0

  if ear < aspect_ratio_min:
      counter += 1
  else:
    if counter >= frame_consec_limit:
      total += 1
    counter = 0

  return (counter, total, leftEye, rightEye)