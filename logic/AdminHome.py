from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys,os

class UI(QFrame):
    def __init__(self):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/AdminHome.ui', self)
        self.setWindowTitle("BALME SSH")
        self.access = self.findChild(QPushButton, "accessControl")
        self.investigate = self.findChild(QPushButton, "investigateTheft")

        self.access.clicked.connect(self.controlAccess)
        self.investigate.clicked.connect(self.investigateFeature)

        # self.show()

    def controlAccess(self):
        print("ACCESS CONTROL FEATURE")

    def investigateFeature(self):
        print('INVESTIGATE FEATURE')
# #--
if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication([])
    
    window = UI()
    window.show()
    app.exec_()