from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys,os
from PyQt5.QtCore import QTimer
import Action


class UI(QFrame):
    def __init__(self):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/EntryDone.ui', self)

        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.returnToHome)

    def showEvent(self, event):
        # Start the timer when the class becomes visible
        self.timer.start(1000)

    def hideEvent(self, event):
        # Stop the timer when the class is not visible
        self.timer.stop()

    def returnToHome(self):
        # Toggle the visibility of the dots
        if(self.counter == 3):
            self.redirectHomeUI = Action.UI()
            self.close()
            self.redirectHomeUI.show()
            self.timer.stop()

        self.counter+=1


# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# app = QApplication(sys.argv)
# window = UI()

# app.exec_()