import sys

# Makes icon work in taskbar on Windows 10/11
import ctypes
myappid = "com.stephencz.wpm.trainer.1.0.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Configure matplotlib for embedded use
import matplotlib
matplotlib.use("Qt5Agg") #Needed for embedding matplotlib in Qt

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
from gui import MainWindow


def main():


  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  app.exec()

if __name__ == "__main__":
  main()