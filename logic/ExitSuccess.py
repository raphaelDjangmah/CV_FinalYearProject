from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys,os
import Action

class UI(QFrame):
    def __init__(self):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/ExitSuccess.ui', self)
        # self.show()

        #get the widgets
        self.checkGood = self.findChild(QCheckBox, "checkbox_good")
        self.checkAvg  = self.findChild(QCheckBox, "checkbox_average")
        self.checkBad  = self.findChild(QCheckBox, "checkbox_bad")

        #pass on click
        self.checkGood.stateChanged.connect(lambda: self.review(3))
        self.checkAvg.stateChanged.connect(lambda: self.review(2))
        self.checkBad.stateChanged.connect(lambda: self.review(1))


    def review(self, input):
        print("REVIEW DONE IS ", input)


        #redirect to home
        self.close()
        self.redirectHomeUi = Action.UI()
        self.redirectHomeUi.show()


# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# app = QApplication(sys.argv)
# window = UI()

# app.exec_()