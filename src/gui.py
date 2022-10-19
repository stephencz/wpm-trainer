import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class SessionInfo():

  def __init__(self):
    self._target_wpm = None
    self._target_time = None

class SessionWidget(QWidget):

  def __init__(self, session, *args, **kwargs):
    super(SessionWidget, self).__init__(*args, **kwargs)
    self._session = session

class MainWindow(QMainWindow):
  
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    # Application Data
    self._target_wpm = 25
    self._target_time = 60
    self._sound_on = True

    # Configure window
    self._app_icon = QIcon()
    self._app_icon.addFile("assets/icon_16.png", QSize(16, 16))
    self._app_icon.addFile("assets/icon_24.png", QSize(24, 24))
    self._app_icon.addFile("assets/icon_32.png", QSize(32, 32))
    self._app_icon.addFile("assets/icon_48.png", QSize(48, 48))
    self._app_icon.addFile("assets/icon_256.png", QSize(256, 256))
    self.setWindowIcon(self._app_icon)

    self.setWindowTitle("WPM Trainer")
    self.setFixedSize(640, 480)

    self._main_widget = QGroupBox()
    self._main_layout = QVBoxLayout()

    # Create options widget and layout
    self._options_widget = QGroupBox()
    self._options_widget.setTitle("Options")
    self._options_layout = QHBoxLayout()
    self._options_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

    # Options line edits and labels
    self._wpm_edit_label = QLabel("WPM:")
    self._wpm_line_edit = QLineEdit()
    self._wpm_line_edit.setText(str(self._target_wpm))
    self._wpm_line_edit.editingFinished.connect(self._handle_wpm_finish_edit)

    self._time_edit_label = QLabel("Minutes: ")
    self._time_line_edit = QLineEdit()
    self._time_line_edit.setText(str(self._target_time))
    self._time_line_edit.editingFinished.connect(self._handle_time_finish_edit)

    # Addwidgets to options
    self._options_layout.addWidget(self._wpm_edit_label)
    self._options_layout.addWidget(self._wpm_line_edit)
    self._options_layout.addWidget(self._time_edit_label)
    self._options_layout.addWidget(self._time_line_edit)  
    self._options_widget.setLayout(self._options_layout)
    self._main_layout.addWidget(self._options_widget)

    # Create control widget and layout
    self._control_widget = QGroupBox()
    self._control_widget.setTitle("Controls")
    self._control_layout = QHBoxLayout()
    self._control_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

    # Control buttons
    self._start_button = QPushButton("Start")
    self._stop_button = QPushButton("Stop")
    self._pause_button = QPushButton("Pause")
    self._reset_button = QPushButton("Reset")

    self._sound_button = QPushButton("Sound On")
    self._sound_button.clicked.connect(self._handle_sound_toggle)

    # Add widgets to control

    self._control_layout.addWidget(self._start_button)
    self._control_layout.addWidget(self._stop_button)
    self._control_layout.addWidget(self._pause_button)
    self._control_layout.addWidget(self._reset_button)
    self._control_layout.addWidget(self._sound_button)
    self._control_widget.setLayout(self._control_layout)
    self._main_layout.addWidget(self._control_widget)

    # Creat content widgets and layouts
    self._content_widget = QGroupBox()
    self._content_widget.setTitle("Session Information")
    self._content_layout = QHBoxLayout()

    self._content_widget.setLayout(self._content_layout)
    self._main_layout.addWidget(self._content_widget)

    self._main_widget.setLayout(self._main_layout)
    self.setCentralWidget(self._main_widget)


  def _handle_sound_toggle(self):
    if self._sound_on:
      self._sound_on = False
      self._sound_button.setText("Sound Off")

    else:
      self._sound_on = True
      self._sound_button.setText("Sound On")

    print(self._sound_on)

  """
  Validates wpm input
  """
  def _handle_wpm_finish_edit(self):
    text = self._wpm_line_edit.text()
    
    if(text.isnumeric()):
      if(int(text) <= 0):
        self._target_wpm = 1
        self._wpm_line_edit.setText(str(self._target_wpm))

      else:
        self._target_wpm = int(text)

    else:
      self._target_wpm = 25
      self._wpm_line_edit.setText(str(self._target_wpm))

 
  """
  Validates time input
  """
  def _handle_time_finish_edit(self):
    text = self._time_line_edit.text()
    
    if(text.isnumeric()):
      if(int(text) <= 0):
        self._target_time = 1
        self._time_line_edit.setText(str(self._target_time))

      else:
        self._target_time = int(text)

    else:
      self._target_time = 60
      self._time_line_edit.setText(str(self._target_time))
      
      


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()