from imutils.video import VideoStream
from face_utils import to_bounding
from blink_detector import blink_detector
from gaze_detector import gaze_detector, get_eyes, detect_pupil
import cv2
import dlib
import time
import imutils

# Initialize HOG-based face detector and create facial landmark predictor
print("[STATUS] Loading face detector...")
detector = dlib.get_frontal_face_detector()

print('[STATUS] Starting camera...')
vs = VideoStream(src=1).start()

prev = counter = total = 0
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
  frame = vs.read()
  frame = imutils.resize(frame, width=400)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  rects = detector(gray, 0)

  for rect in rects:
    (bX, bY, bW, bH) = to_bounding(rect)
    cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH), (0, 255, 0), 1) # draw bounding box

    counter, total, leftEye, rightEye = blink_detector(
      img=gray, 
      rect=rect,
      counter=counter, 
      total=total, 
    )
    detected_eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
    eyes = get_eyes(detected_eyes, frame.shape)

    for (ex, ey, ew, eh) in eyes:
        eye_roi = gray[ey:ey + eh, ex:ex + ew]
        pupil_center, pupil_radius = detect_pupil(eye_roi)

        if pupil_center and pupil_radius:
            cv2.circle(frame, (ex + pupil_center[0], ey + pupil_center[1]), pupil_radius, (255, 0, 0), 1)
            gaze_detector(frame, (ex, ey), pupil_center, (ew, eh))


    for (x, y) in leftEye:
      cv2.circle(frame, (x, y), 1, (0, 0, 255, -1))

    for (x, y) in rightEye:
      cv2.circle(frame, (x, y), 1, (0, 0, 255, -1))

    cv2.putText(frame, "Blinks: {}".format(total), (10, 30),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    
  
  cv2.imshow("Frame", frame)
  key = cv2.waitKey(1) & 0xFF

  if key == ord('q'): break
  elif key == ord('c'): total = 0
cv2.destroyAllWindows()
vs.stop()
