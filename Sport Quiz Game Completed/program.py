#GUI imports
import sys
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
#function imports
from main import frame1, frame2, frame3, frame4, grid

#initiallize GUI application
app = QApplication(sys.argv)

#window and settings
window = QWidget()
window.setWindowTitle("only true sports fans can win this quiz")
window.setWindowIcon(QtGui.QIcon('images/icon.ico'))
#place window in (x,y) coordinates
# window.move(2700, 200)
window.setStyleSheet("background: #eeeded;")

#display frame 1
frame1()
window.setLayout(grid)
window.showFullScreen()
time.sleep(2)
window.showMaximized()

window.show()
sys.exit(app.exec()) #terminate the app