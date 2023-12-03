from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from gtts import gTTS

import sys
import os

class Widget(QWidget):
  def __init__(self, parent=None):
    super(Widget, self).__init__(parent)

    self.setWindowTitle("vision unLocked")

    layout = QGridLayout()
    self.setLayout(layout)

    self.hello = QPushButton('Hello')
    self.hello.clicked.connect(lambda: self.greetings("Hello"))

    self.world = QPushButton('World')
    self.world.clicked.connect(lambda: self.greetings('World'))

    layout.addWidget(self.hello, 0, 0,
                     alignment=Qt.AlignmentFlag.AlignTop)
    layout.addWidget(self.world, 1, 0,
                     alignment=Qt.AlignmentFlag.AlignBottom)

  def greetings(self, string):
    speech = gTTS(text=string, lang='en', slow=False)
    speech.save("text.mp3")
    os.system("afplay text.mp3")
    

if __name__ == "__main__":
  app = QApplication()
  
  w = Widget()
  w.show()
  w.resize(800, 600)

  with open("sample/display/style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

  sys.exit(app.exec())
