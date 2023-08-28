from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys,os
from AwaitCam import UI as AwaitCamera
from model.Model import TakePhoto as WebCam
import cv2
from datetime import datetime
import Action

#from model.Model import ExtractObjects as ExtractItems



class UI(QFrame):
    def __init__(self, data):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/IDInput.ui', self)

        #
        self.intent = data
        
        #defining widgets
        self.idDisplay = self.findChild(QLabel, "id_number")
        self.idClear   = self.findChild(QPushButton, "id_clearer")
        self.id9       = self.findChild(QPushButton, "id_9")
        self.id8       = self.findChild(QPushButton, "id_8")
        self.id7       = self.findChild(QPushButton, "id_7")
        self.id6       = self.findChild(QPushButton, "id_6")
        self.id5       = self.findChild(QPushButton, "id_5")
        self.id4       = self.findChild(QPushButton, "id_4")
        self.id3       = self.findChild(QPushButton, "id_3")
        self.id2       = self.findChild(QPushButton, "id_2")
        self.id1       = self.findChild(QPushButton, "id_1")
        self.id0       = self.findChild(QPushButton, "id_0")
        self.idFinish  = self.findChild(QPushButton, "id_finish")
        self.backBtn   = self.findChild(QPushButton, "backBtn")
        self.toastLabel= self.findChild(QLabel, "label_toast")
        self.toastLabel.hide()

        #add the click functionalites to each
        self.idClear.clicked.connect(self.clearer)
        self.idFinish.clicked.connect(self.done)
        self.id9.clicked.connect(lambda: self.input(9))
        self.id8.clicked.connect(lambda: self.input(8))
        self.id7.clicked.connect(lambda: self.input(7))
        self.id6.clicked.connect(lambda: self.input(6))
        self.id5.clicked.connect(lambda: self.input(5))
        self.id4.clicked.connect(lambda: self.input(4))
        self.id3.clicked.connect(lambda: self.input(3))
        self.id2.clicked.connect(lambda: self.input(2))
        self.id1.clicked.connect(lambda: self.input(1))
        self.id0.clicked.connect(lambda: self.input(0))
        self.backBtn.clicked.connect(self.backClicked)
        
    def backClicked(self):
        self.backPageUI = Action.UI()
        self.close()
        self.backPageUI.show()

    def done(self):
        #take student ID 
        inputText = self.idDisplay.text()
        try:
            studentID = int(inputText)
        except:
            return

        data = [studentID, self.intent]

        #not opening camera if the user's photos
        self.dateNow = (datetime.now()).date()

        entryExitTag = "entry"
        entryExitOp = "exit"
        if(data[1] == 0):
            entryExitTag = "exit"
            entryExitOp = "entry"
        self.directory = f'./../data/ObjectsDetected/{self.dateNow}/{data[0]}/{entryExitTag}/fullImage.png'

        #check if the login contains numbers
        if(len(str(studentID)) != 8):
            self.toastLabel.setStyleSheet('font: 7pt "Fredoka"; border: 1px solid #000; background-color:#d63384; border-radius: 10px; color: #fff;padding: 10px;')
            self.toastLabel.setText('Invalid ID Length')
            self.toastLabel.show()
            return
        
        #for exit, make sure the entry exits
        self.directoryOp = f'./../data/ObjectsDetected/{self.dateNow}/{data[0]}/{entryExitOp}/fullImage.png'
        if (data[1] == 0 and not os.path.isfile(self.directoryOp)):
            self.toastLabel.setStyleSheet('font: 7pt "Fredoka"; border: 1px solid #000; background-color:#fd7e14; border-radius: 10px; color: #000;padding: 10px;')
            self.toastLabel.setText('Please check in First!')
            self.toastLabel.show()
            return
        
        #restricting entry access to some ids
        if(data[1] == 1):
            restricted = []
            fileData = ""
            with open('./../data/restrictedUsers.csv', 'r') as f:
                fileData = f.read()
            
            restricted = fileData.split('\n')
            for id in restricted:
                if(str(studentID) == id):
                    self.toastLabel.setStyleSheet('font: 7pt "Fredoka"; border: 1px solid #000; background-color:#ff0000; border-radius: 10px; color: #fff;padding: 10px;')
                    self.toastLabel.setText('You have been restricted Access')
                    self.toastLabel.show()
                    return

            #also make sure an entry record does not already exist!---------------------- SUBJECT TO CHANGE -----------------------
            if(os.path.isfile(self.directory)):
                self.toastLabel.setStyleSheet('font: 7pt "Fredoka"; border: 1px solid #000; background-color:#4BB543; border-radius: 10px; color: #fff;padding: 10px;')
                self.toastLabel.setText('You already checked in today')
                self.toastLabel.show()
                return


        #navigating to next page
        self.toastLabel.show()
        self.camWaitUI = AwaitCamera(data)
        #navigate to the webcam loading screen
        self.close()    
        self.camWaitUI.show()
        
        #opening webcam
        if(not os.path.isfile(self.directory)):            
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)

            #open webcam
            WebCam.take(WebCam(), data[0], data[1])

            # Close the main application window
            cv2.destroyAllWindows()

    def clearer(self):
        self.idDisplay.setText("Enter ID")
        
    def input(self, value):
        
        #already existing
        try:
            existing = int(self.idDisplay.text())
            current  = str(existing)+str(value)
            self.idDisplay.setText(str(current))

        except:
            self.idDisplay.setText(str(value))

# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# app = QApplication(sys.argv)
# window = UI()

# app.exec_()