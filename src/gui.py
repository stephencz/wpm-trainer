import sys
from enum import Enum
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class SessionState(Enum):
  NONE = 1
  ACTIVE = 2
  PAUSED = 3
  FINISHED = 4

class SessionWidget(QWidget):

  def __init__(self, session, *args, **kwargs):
    super(SessionWidget, self).__init__(*args, **kwargs)
    self._session = session

class MainWindow(QMainWindow):
  
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    # Application Data
    self.session_state = SessionState.NONE
    self.session_data = []
    self.target_wpm = 25
    self.target_time = 60
    self.sound_on = True


    # Configure window
    self.app_icon = QIcon()
    self.app_icon.addFile("assets/icon_16.png", QSize(16, 16))
    self.app_icon.addFile("assets/icon_24.png", QSize(24, 24))
    self.app_icon.addFile("assets/icon_32.png", QSize(32, 32))
    self.app_icon.addFile("assets/icon_48.png", QSize(48, 48))
    self.app_icon.addFile("assets/icon_256.png", QSize(256, 256))
    self.setWindowIcon(self.app_icon)

    self.setWindowTitle("WPM Trainer")
    self.setFixedSize(640, 480)

    self.main_widget = QGroupBox()
    self.main_layout = QVBoxLayout()

    # Create options widget and layout
    self.options_widget = QGroupBox()
    self.options_widget.setTitle("Options")
    self.options_layout = QHBoxLayout()
    self.options_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

    # Options line edits and labels
    self.wpm_edit_label = QLabel("WPM:")
    self.wpm_line_edit = QLineEdit()
    self.wpm_line_edit.setText(str(self.target_wpm))
    self.wpm_line_edit.editingFinished.connect(self.handle_wpm_finish_edit)

    self.time_edit_label = QLabel("Minutes: ")
    self.time_line_edit = QLineEdit()
    self.time_line_edit.setText(str(self.target_time))
    self.time_line_edit.editingFinished.connect(self.handle_time_finish_edit)

    # Addwidgets to options
    self.options_layout.addWidget(self.wpm_edit_label)
    self.options_layout.addWidget(self.wpm_line_edit)
    self.options_layout.addWidget(self.time_edit_label)
    self.options_layout.addWidget(self.time_line_edit)  
    self.options_widget.setLayout(self.options_layout)
    self.main_layout.addWidget(self.options_widget)

    # Create control widget and layout
    self.control_widget = QGroupBox()
    self.control_widget.setTitle("Controls")
    self.control_layout = QHBoxLayout()
    self.control_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

    # Control buttons
    self.start_button = QPushButton("Start")
    self.start_button.clicked.connect(self.handle_start_session)

    self.stop_button = QPushButton("Pause")
    self.stop_button.clicked.connect(self.handle_pause_session)
    
    self.reset_button = QPushButton("Reset")
    self.reset_button.clicked.connect(self.handle_reset_session)

    self.sound_button = QPushButton("Sound On")
    self.sound_button.clicked.connect(self.handle_sound_toggle)

    # Add widgets to control
    self.control_layout.addWidget(self.start_button)
    self.control_layout.addWidget(self.stop_button)
    self.control_layout.addWidget(self.pause_button)
    self.control_layout.addWidget(self.reset_button)
    self.control_layout.addWidget(self.sound_button)
    self.control_widget.setLayout(self.control_layout)
    self.main_layout.addWidget(self.control_widget)

    # Creat content widgets and layouts
    self.content_widget = QGroupBox()
    self.content_widget.setTitle("Session Information")
    self.content_layout = QHBoxLayout()

    self.content_widget.setLayout(self.content_layout)
    self.main_layout.addWidget(self.content_widget)

    self.main_widget.setLayout(self.main_layout)
    self.setCentralWidget(self.main_widget)


  """
  Start a new training session.
  """
  def handle_start_session(self):
    self.session_state = SessionState.ACTIVE

  """
  Pauses the current training session.
  """
  def handle_pause_session(self):
    self.session_state = SessionState.PAUSED

  """
  Resets the current training session.
  """
  def handle_reset_session(self):
    self.session_data = []
    self.session_state = SessionState.NONE

  """
  Toggles sound on/off.
  """
  def handle_sound_toggle(self):
    if self.sound_on:
      self.sound_on = False
      self.sound_button.setText("Sound Off")

    else:
      self.sound_on = True
      self.sound_button.setText("Sound On")

  """
  Validates wpm input
  """
  def handle_wpm_finish_edit(self):
    text = self.wpm_line_edit.text()
    
    if(text.isnumeric()):
      if(int(text) <= 0):
        self.target_wpm = 1
        self.wpm_line_edit.setText(str(self.target_wpm))

      else:
        self.target_wpm = int(text)

    else:
      self.target_wpm = 25
      self.wpm_line_edit.setText(str(self.target_wpm))

 
  """
  Validates time input
  """
  def handle_time_finish_edit(self):
    text = self.time_line_edit.text()
    
    if(text.isnumeric()):
      if(int(text) <= 0):
        self.target_time = 1
        self.time_line_edit.setText(str(self.target_time))

      else:
        self.target_time = int(text)

    else:
      self.target_time = 60
      self.time_line_edit.setText(str(self.target_time))
      
      


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()