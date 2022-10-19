import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
  
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)
    self.setWindowTitle("WPM Trainer")
    self.setFixedSize(480, 360)

    self._main_widget = QWidget()
    self._main_layout = QVBoxLayout()

    # Create options widget and layout
    self._options_widget = QWidget()
    self._options_layout = QHBoxLayout()

    # Options line edits and labels
    self._wpm_input_label = QLabel("WPM")
    self._wpm_line_edit = QLineEdit()

    self._time_input_label = QLabel("Minutes")
    self._time_line_edit = QLineEdit()

    # Options buttons
    self._start_button = QPushButton("Start")
    self._stop_button = QPushButton("Stop")
    self._pause_button = QPushButton("Pause")
    self._reset_button = QPushButton("Reset")
    self._sound_button = QPushButton("Sound Off")

    # Addwidgets to options
    self._options_layout.addWidget(self._wpm_input_label)
    self._options_layout.addWidget(self._wpm_line_edit)

    self._options_layout.addWidget(self._time_input_label)
    self._options_layout.addWidget(self._time_line_edit)

    self._options_layout.addWidget(self._start_button)
    self._options_layout.addWidget(self._stop_button)
    self._options_layout.addWidget(self._pause_button)
    self._options_layout.addWidget(self._reset_button)
    self._options_layout.addWidget(self._sound_button)

    self._options_widget.setLayout(self._options_layout)
    self._main_layout.addWidget(self._options_widget)

    # --

    self._main_widget.setLayout(self._main_layout)
    self.setCentralWidget(self._main_widget)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()