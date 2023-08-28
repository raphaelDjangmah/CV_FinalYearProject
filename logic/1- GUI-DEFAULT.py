from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys,os



class UI(QFrame):
    def __init__(self):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('AppDefault.ui', self)
        self.setWindowTitle("BALME SSH")

        self.show()

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
window = UI()

app.exec_()