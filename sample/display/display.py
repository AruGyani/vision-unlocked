from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

import sys

class Widget(QWidget):
  def __init__(self, parent=None):
    super(Widget, self).__init__(parent)

    push_button = QPushButton("Hello")

    layout = QGridLayout()
    self.setLayout(layout)

if __name__ == "__main__":
  app = QApplication()
  
  w = Widget()
  w.show()
  w.resize(800, 600)

  with open("style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

  sys.exit(app.exec())
