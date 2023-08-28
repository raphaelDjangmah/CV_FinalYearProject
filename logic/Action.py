from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys,os
from IDInput import UI as EntryUI
from EntryDone import UI as ExitUI


class UI(QFrame):
    def __init__(self):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/ActionState.ui', self)
        self.setWindowTitle("BALME SSH")

        self.entryBtn = self.findChild(QPushButton, "entryButton")
        self.exitBtn = self.findChild(QPushButton, "exitButton")

        self.entryBtn.clicked.connect(self.enterLibrary)
        self.exitBtn.clicked.connect(self.exitLibrary)
        
        #creating instances
        self.entryUI = EntryUI(1)  
        self.exitUI = EntryUI(0)  

        self.show()

    def enterLibrary(self):
        print('INITIATING LIBRARY ENTRY')
        self.close()
        self.entryUI.show()

    def exitLibrary(self):
        print('INITIATING LIBRARY EXIT')
        self.close()
        self.exitUI.show()




#--
# if __name__ == "__main__":
#     os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
#     app = QApplication([])
    
#     window = UI()
#     window.show()
#     app.exec_()