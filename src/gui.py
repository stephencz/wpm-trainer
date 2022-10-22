import datetime
from enum import Enum
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from keylisten import KeyboardListener

class SessionState(Enum):
  NONE = 1
  ACTIVE = 2
  PAUSED = 3

class SessionIntervalData():

  def __init__(self, wpm):
    self._wpm = wpm

  @property
  def wpm(self):
    return self._wpm

  @wpm.setter
  def wpm(self, wpm):
    self._wpm = wpm

class SessionPlot(FigureCanvasQTAgg):

  def __init__(self, target_wpm, target_time, data, parent=None, width=4, height=2, dpi=100):    
    
    self.target_wpm = target_wpm
    self.target_time = target_time

    self.data = data
    self.fig = Figure(figsize=(width, height), dpi=dpi)

    self.ax1 = self.fig.add_subplot(1, 1, 1)

    self.ax1.set_facecolor((0.0, 0.0, 0.0, 1.0))

    self.ax1.set_xlabel("Time")
    self.ax1.set_ylabel("WPM")

    self.ax1.set_xbound(target_time)
    self.ax1.set_ybound(target_wpm)

    super(SessionPlot, self).__init__(self.fig)

  def update_plot(self):
    for item in self.data:
      interval = item['interval']
      word_count = item['word_count']

      if word_count < self.target_wpm:
        self.ax1.bar(interval, word_count, color=(1.0, 0.0, 0.0, 1.0))

      else:
        self.ax1.bar(interval, word_count, color=(0.0, 1.0, 0.0, 1.0))

    self.fig.canvas.draw()
    self.fig.canvas.flush_events()

class MainWindow(QMainWindow):
  
  TIMER_TICK_RATE = 1000

  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    # Application Data
    self.session_state = SessionState.NONE
    self.session_interval_data = []

    self.intervals_passed = 0
    self.seconds_in_interval = 0 

    self.target_wpm = 25
    self.target_time = 60

    self.sound_on = True

    self.keyboard_listener = KeyboardListener()

    # Configure window
    self.app_icon = QIcon()
    self.app_icon.addFile("assets/icon_16.png", QSize(16, 16))
    self.app_icon.addFile("assets/icon_24.png", QSize(24, 24))
    self.app_icon.addFile("assets/icon_32.png", QSize(32, 32))
    self.app_icon.addFile("assets/icon_48.png", QSize(48, 48))
    self.app_icon.addFile("assets/icon_256.png", QSize(256, 256))
    self.setWindowIcon(self.app_icon)

    self.setWindowTitle("WPM Trainer | 0:00:00 | 0 words")
    self.setFixedSize(480, 640)

    self.main_widget = QGroupBox()
    self.main_layout = QVBoxLayout()

    # Configure the QTimer that will be used to control sessions
    self.timer = QTimer()
    self.timer.timeout.connect(self.handle_timeout)

    # Load the chime and buzzer sound effects
    self.chime_sound = QSoundEffect()
    self.chime_sound.setSource(QUrl.fromLocalFile("assets/chime.wav"))

    self.buzzer_sound = QSoundEffect()
    self.buzzer_sound.setSource(QUrl.fromLocalFile("assets/buzzer.wav"))

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

    self.stop_button = QPushButton("Stop")
    self.stop_button.setEnabled(False)
    self.stop_button.clicked.connect(self.handle_stop_session)
    
    self.reset_button = QPushButton("Reset")
    self.reset_button.clicked.connect(self.handle_reset_session)

    self.sound_button = QPushButton("Sound On")
    self.sound_button.clicked.connect(self.handle_sound_toggle)

    # Add widgets to control
    self.control_layout.addWidget(self.start_button)
    self.control_layout.addWidget(self.stop_button)
    self.control_layout.addWidget(self.reset_button)
    self.control_layout.addWidget(self.sound_button)
    self.control_widget.setLayout(self.control_layout)
    self.main_layout.addWidget(self.control_widget)

    # Creat content widgets and layouts
    self.content_widget = QGroupBox()
    self.content_widget.setTitle("Session Information")

    # Create Tab widget and layout for GroupBox
    self.content_layout = QHBoxLayout()
    self.content_tab = QTabWidget()
    self.content_layout.addWidget(self.content_tab)

    # Configure Graph Tab 
    self.session_plot_widget = QWidget()
    self.session_plot_layout = QHBoxLayout()
    self.session_plot = SessionPlot(target_wpm=self.target_wpm, target_time=self.target_time, data=self.session_interval_data)

    self.session_plot_layout.addWidget(self.session_plot)
    self.session_plot_widget.setLayout(self.session_plot_layout)
    self.content_tab.addTab(self.session_plot_widget, "Graph")

    # Statistics Tab
    self.statistics_tab_widget = QWidget()
    self.statistics_tab_layout = QGridLayout()

    self.current_interval_label = QLabel()
    self.current_interval_label.setText("Interval: ")

    self.statistics_tab_layout.addWidget(self.current_interval_label, 0, 0)

    self.statistics_tab_widget.setLayout(self.statistics_tab_layout)
    self.content_tab.addTab(self.statistics_tab_widget, "Statistics")

    self.content_widget.setLayout(self.content_layout)
    self.main_layout.addWidget(self.content_widget)

    self.main_widget.setLayout(self.main_layout)
    self.setCentralWidget(self.main_widget)


  def handle_timeout(self):
    if self.intervals_passed >= self.target_time:
      self.keyboard_listener.release_listener()
      self.timer.stop()

    else:

      if self.seconds_in_interval >= 60:
        self.intervals_passed += 1
        self.seconds_in_interval = 0
        
        self.session_interval_data.append({
          'interval': self.intervals_passed, 
          'word_count': self.keyboard_listener.word_count
          })


        self.keyboard_listener.input = ""
        self.keyboard_listener.word_count = 0

        self.session_plot.data = self.session_interval_data
        self.session_plot.update_plot()

        if self.sound_on :
          if self.session_interval_data[self.intervals_passed - 1]['word_count'] >= self.target_wpm:
            self.chime_sound.play()

          else:
            self.buzzer_sound.play()

      else:
        self.seconds_in_interval += 1

      seconds_passed = (self.intervals_passed * 60) + self.seconds_in_interval
      formatted_time = str(datetime.timedelta(seconds=seconds_passed))
      word_count = self.keyboard_listener.word_count


      self.setWindowTitle("WPM Trainer | {0} | {1} words".format(formatted_time, word_count))


  """
  Start a new training session.
  """
  def handle_start_session(self):
    if self.session_state == SessionState.PAUSED:
      self.session_state = SessionState.ACTIVE
      self.start_button.setEnabled(False)
      self.stop_button.setEnabled(True)
      self.keyboard_listener.enabled = True
      self.timer.start(self.TIMER_TICK_RATE)

    else:
      if self.session_state != SessionState.ACTIVE:
        self.session_state = SessionState.ACTIVE
        self.intervals_passed = 0
        self.seconds_in_interval = 0

        # Disable and enable widgets
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.wpm_line_edit.setEnabled(False)
        self.time_line_edit.setEnabled(False)

        # Update plot to represent new session optiosn
        self.session_plot_layout.removeWidget(self.session_plot)
        self.session_plot = SessionPlot(self.target_wpm, self.target_time, self.session_interval_data)
        self.session_plot_layout.addWidget(self.session_plot)

        self.keyboard_listener.create_listener()
        self.timer.start(self.TIMER_TICK_RATE)

  """
  Stop the current training session.
  """
  def handle_stop_session(self):
    self.session_state = SessionState.PAUSED
    self.start_button.setEnabled(True)
    self.stop_button.setEnabled(False)
    self.keyboard_listener.enabled = False
    self.timer.stop()
    

  """
  Resets the current training session.
  """
  def handle_reset_session(self):
    self.setWindowTitle("WPM Trainer | 0:00:00 | 0 words")

    self.session_state = SessionState.NONE
    self.intervals_passed = 0
    self.seconds_in_interval = 0
    self.session_interval_data = []

    self.start_button.setEnabled(True)
    self.stop_button.setEnabled(False)
    self.wpm_line_edit.setEnabled(True)
    self.time_line_edit.setEnabled(True)

    self.keyboard_listener.release_listener()
    self.keyboard_listener.reset()
    self.timer.stop()

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

    


