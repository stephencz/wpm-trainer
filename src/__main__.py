import sys

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