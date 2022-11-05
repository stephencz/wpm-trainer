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

class ApplicationData():
  """
  The ApplicationData object is a wrapper for all data that
  the application needs to keep track of during its lifetime.
  """

  def __init__(self):
    
    self._session_state = SessionState.NONE
    """The state of the current session. See SessionState enum."""

    self._session_interval_data = []
    """An array of dicts containing information about session's intervals."""

    self._intervals_passed = 0
    """The number of intervals passed in the session."""

    self._seconds_in_interval = 0 
    """The seconds in the current interval."""

    self._target_wpm = 25
    """The number of words the user is trying to write per minute."""

    self._target_time = 60
    """The time in minutes, or number of minute long intervals, the user is writing for."""

    self._keyboard_listener = KeyboardListener()
    """KeyboardListener object for determining wpm."""

    self._sound_on = True
    """True sound is on. False sound is off."""

  @property
  def session_state(self):
    return self._session_state

  @session_state.setter
  def session_state(self, state):
    self._session_state = state

  @property
  def session_interval_data(self):
    return self._session_interval_data

  @session_interval_data.setter
  def session_interval_data(self, data):
    self._session_interval_data = data

  @property
  def intervals_passed(self):
    return self._intervals_passed

  @intervals_passed.setter
  def intervals_passed(self, intervals):
    self._intervals_passed = intervals

  @property
  def target_wpm(self):
    return self._target_wpm

  @target_wpm.setter
  def target_wpm(self, wpm):
    self._target_time = wpm

  @property
  def target_time(self):
    return self._target_time

  @target_time.setter
  def target_time(self, time):
    self._target_time = time

  @property
  def keyboard_listener(self):
    return self._keyboard_listener

  @property
  def sound_on(self):
    return self._sound_on

  @sound_on.setter
  def sound_on(self, state):
    self._sound_on = state

class SessionMenuBarWidget(QWidget):

  def __init__(self, appdata, *args, **kwargs):
    super(SessionMenuBarWidget, self).__init__(*args, *kwargs)
    self._appdata = appdata

    # Create menu bar
    self.menu_bar = QMenuBar()
    self.file_menu = self.menu_bar.addMenu("File")
    self.presets_menu = self.menu_bar.addMenu("Presets")
    self.about_menu = self.menu_bar.addMenu("About")
    
    self.preset_500_wpm = self.presets_menu.addAction("500 WPH")
    self.preset_500_wpm.triggered.connect(lambda: self.set_preset(8, 60))

    self.preset_600_wpm = self.presets_menu.addAction("600 WPH")
    self.preset_600_wpm.triggered.connect(lambda: self.set_preset(10, 60))

    self.preset_800_wpm = self.presets_menu.addAction("800 WPH")
    self.preset_800_wpm.triggered.connect(lambda: self.set_preset(13, 60))

    self.preset_1000_wpm = self.presets_menu.addAction("1000 WPH")
    self.preset_1000_wpm.triggered.connect(lambda: self.set_preset(17, 60))

    self.preset_1500_wpm = self.presets_menu.addAction("1500 WPH")
    self.preset_1500_wpm.triggered.connect(lambda: self.set_preset(25, 60))

    self.preset_2000_wpm = self.presets_menu.addAction("2000 WPH")
    self.preset_2000_wpm.triggered.connect(lambda: self.set_preset(33, 60))

    self.preset_2500_wpm = self.presets_menu.addAction("2500 WPH")
    self.preset_2500_wpm.triggered.connect(lambda: self.set_preset(42, 60))

    self.preset_3000_wpm = self.presets_menu.addAction("3000 WPH")
    self.preset_3000_wpm.triggered.connect(lambda: self.set_preset(50, 60))

    self.preset_4000_wpm = self.presets_menu.addAction("4000 WPH")
    self.preset_4000_wpm.triggered.connect(lambda: self.set_preset(67, 60))

    self.preset_5000_wpm = self.presets_menu.addAction("5000 WPH")
    self.preset_5000_wpm.triggered.connect(lambda: self.set_preset(83, 60))

    self.preset_6000_wpm = self.presets_menu.addAction("6000 WPH")
    self.preset_6000_wpm.triggered.connect(lambda: self.set_preset(100, 60))

    # Create signal for preset being changed.
    self.preset_changed = pyqtSignal([int], [int])
  
  def set_preset(self, wpm, time):
    if(self._appdata.session_state == SessionState.NONE):
      self._appdata.target_wpm = wpm
      self._appdata.target_time = time
      self.preset_changed.emit(self._appdata.target_wpm, self._appdata.target_time)

      # How do I get the MenuBar widget to set the text of the SessionOptionsWidget when
      # changed? This is an issue I need to figure out how to solve it.s
      # self.wpm_line_edit.setText(str(self.target_wpm))
      # self.time_line_edit.setText(str(self.target_time))

class SessionOptionsWidget(QWidget):
  """
  The SessionOptionsWidget provides the functionality for setting
  the applications target words per minute and target time in minutes
  for the next training session.
  """
  
  def __init__(self, appdata, *args, **kwargs):
    super(SessionOptionsWidget, self).__init__(*args, **kwargs)

class SessionControlsWidget(QWidget):
  pass

class SessionInformationWidget(QWidget):
  pass

class SessionPlot(FigureCanvasQTAgg):

  def __init__(self, target_wpm, target_time, data, parent=None, width=4, height=2, dpi=100):    
    
    self.target_wpm = target_wpm
    self.target_time = target_time

    self.data = data
    self.fig = Figure(figsize=(width, height), dpi=dpi)

    self.ax1 = self.fig.add_subplot(1, 1, 1)

    self.ax1.set_facecolor((0.0, 0.0, 0.0, 1.0))

    self.ax1.set_title("Time: 0:00:00  Words: 0")

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

    self._appdata = ApplicationData()

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

    
    # Create Widgets
    self.main_widget = QGroupBox()
    self.main_layout = QVBoxLayout()

    self.menu_bar = SessionMenuBarWidget(appdata=self._appdata)

    self.main_layout.addWidget(self.menu_bar)

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

    self.current_interval_value_label = QLabel()
    self.current_interval_value_label.setText("1")

    self.current_time_label = QLabel()
    self.current_time_label.setText("Session Time: ")

    self.current_time_value_label = QLabel()
    self.current_time_value_label.setText("0:00:0")

    self.statistics_tab_layout.addWidget(self.current_time_label, 0, 0)
    self.statistics_tab_layout.addWidget(self.current_time_value_label, 0 , 1)
    self.statistics_tab_layout.addWidget(self.current_interval_label, 1, 0)
    self.statistics_tab_layout.addWidget(self.current_interval_value_label, 1, 1)

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

        self.current_interval_value_label.setText(str(self.intervals_passed + 1))

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
      self.session_plot.ax1.set_title("Time: {0}  Words: {1}".format(formatted_time, word_count))
      self.current_time_value_label.setText(formatted_time)

      self.session_plot.fig.canvas.draw()
      self.session_plot.fig.canvas.flush_events()

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

    self.current_interval_value_label.setText("1")

    self.keyboard_listener.release_listener()
    self.keyboard_listener.reset()
    self.timer.stop()

    self.session_plot.ax1.set_title("Time: 0:00:00  Words: 0")
    self.session_plot.data = self.session_interval_data
    self.session_plot.update_plot()
    
    self.session_plot.fig.canvas.draw()
    self.session_plot.fig.canvas.flush_events()

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

    


