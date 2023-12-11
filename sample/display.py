from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from gtts import gTTS

from imutils.video import VideoStream
from face_utils import to_bounding
from blink_detector import blink_detector
from gaze_detector import gaze_detector, get_eyes, detect_pupil

import cv2
import dlib
import time
import imutils
import os
import sys

class MainWindow(QWidget):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.timer = time.time()

    self.layout = QVBoxLayout()

    self.Option1 = QPushButton('Hello')
    self.Option1.clicked.connect(lambda: self.greetings("Hello"))
    self.layout.addWidget(self.Option1)

    self.FeedLabel = QLabel()
    self.layout.addWidget(self.FeedLabel)

    self.Option2 = QPushButton('World')
    self.Option2.clicked.connect(lambda: self.greetings("World"))
    self.layout.addWidget(self.Option2)

    self.Worker1 = Worker1()
    self.Worker1.start()
    self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
    self.Worker1.BlinkDetected.connect(self.BlinkDetectedSlot)
    
    self.setLayout(self.layout)

  # Text to Speech Interaction
  # ("afplay" is a MacOS-specific command. Please switch this to the command appropriate for your operating system)
  def greetings(self, string):
    speech = gTTS(text=string, lang='en', slow=False)
    speech.save(f"sample/display/{string.lower()}.mp3")
    os.system(f"afplay sample/display/{string.lower()}.mp3")

  def ImageUpdateSlot(self, Image):
    self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

  def BlinkDetectedSlot(self):
    current = time.time()
    
    if current - self.timer >= 2:
      self.Option1.click()
      self.timer = current
    

  def CancelFeed(self):
    self.Worker1.stop()

class Worker1(QThread):
  ImageUpdate = Signal(QImage)
  BlinkDetected = Signal()
  
  detector = dlib.get_frontal_face_detector()
  prev = counter = total = 0
  eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

  def run(self):
    self.ThreadActive = True
    Capture = VideoStream(src=0).start()

    while self.ThreadActive:
      frame = Capture.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      rects = self.detector(gray, 0)

      for rect in rects:
          (bX, bY, bW, bH) = to_bounding(rect)
          cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH), (0, 255, 0), 1) # draw bounding box

          self.counter, self.total, leftEye, rightEye = blink_detector(
            img=gray, 
            rect=rect,
            counter=self.counter, 
            total=self.total, 
          )

          if self.prev < self.total:
            self.BlinkDetected.emit()

          self.prev = self.total

          detected_eyes = self.eye_cascade.detectMultiScale(gray, 1.1, 4)
          eyes = get_eyes(detected_eyes, frame.shape)

          for (ex, ey, ew, eh) in eyes:
              eye_roi = gray[ey:ey + eh, ex:ex + ew]
              pupil_center, pupil_radius = detect_pupil(eye_roi)

              if pupil_center and pupil_radius:
                  cv2.circle(frame, (ex + pupil_center[0], ey + pupil_center[1]), pupil_radius, (255, 0, 0), 1)
                  gaze_detector(frame, (ex, ey), pupil_center, (ew, eh))

          for (x, y) in leftEye:
            cv2.circle(frame, (x, y), 4, (0, 0, 255, -1))

          for (x, y) in rightEye:
            cv2.circle(frame, (x, y), 4, (0, 0, 255, -1))

          cv2.putText(frame, "Blinks: {}".format(self.total), (20, 50),
                      cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 4)

      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
      picture = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
      self.ImageUpdate.emit(picture)
    Capture.release()

  def stop(self):
    self.ThreadActive = False
    self.quit()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  root = MainWindow()
  root.show()

  with open("sample/display/style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

  sys.exit(app.exec())