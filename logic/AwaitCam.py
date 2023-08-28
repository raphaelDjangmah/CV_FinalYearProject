from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys,os,time
from itemConfirm import UI as ConfirmItem
from EntryDone import UI as EntrySuccess
from ExitSuccess import UI as ExitSuccess
from EntryDone import UI as Exit
from model.Model import TakePhoto as WebCam
from model.Model import ExtractObjects as ExtractItems
from model.PictureAlgorithms import Algorithms 
from datetime import datetime
import cv2
from model.Utilities import Databases as db;

class UI(QFrame):
    def __init__(self, data):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/AwaitingWebcam.ui', self)
        self.setWindowTitle("BALME SSH")
        
        self.intent = data
        self.dateNow = (datetime.now()).date()

        entryExitTag = "entry"
        if(self.intent[1] == 0):
            entryExitTag = "exit"

        self.directory = f'./../data/ObjectsDetected/{self.dateNow}/{self.intent[0]}/{entryExitTag}/person.png'
        self.directoryB = f'./../data/ObjectsDetected/{self.dateNow}/{self.intent[0]}/{entryExitTag}/fullImage.png'

        #identify widgets
        self.circle1 = self.findChild(QLabel, "waiting_indicator_1")
        self.circle2 = self.findChild(QLabel, "waiting_indicator_2")
        self.circle3 = self.findChild(QLabel, "waiting_indicator_3")
        self.frame   = self.findChild(QFrame, "Frame")
        self.status  = self.findChild(QLabel, "status_label")
        self.extracted = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateIndicator)

    def showEvent(self, event):
        # Start the timer when the class becomes visible
        self.timer.start(1000)

    def hideEvent(self, event):
        # Stop the timer when the class is not visible
        self.timer.stop()
        
    def updateIndicator(self):

        #if a file exists, close the loop
        if not os.path.isfile(self.directory):
            #extract the items

            if(os.path.isfile(self.directoryB)):
                ExtractItems().extract(self.intent[0], self.intent[1])

            if(self.intent[1] == 1 and os.path.isfile(self.directoryB)):
                self.close()
                self.itemsConfirmUI = ConfirmItem(self.intent)
                self.itemsConfirmUI.show()
        else:
            print("intent is ",self.intent)
            if(self.intent[1] == 1):
                self.close()
                self.entryDoneUI = EntrySuccess()
                self.entryDoneUI.show()
                
            else:
                self.status.setText("RETRIEVING ITEMS LINKED ON YOU ON ENTRY")
                self.status.setStyleSheet("color:#008000; font-weight:bold; font-family:Fredoka")
                
                #get the items
                onEntryItems = self.retrieveItems(1)
                onExitItems  = self.retrieveItems(0)
                
                #
                verifySuccess = self.verify(onEntryItems, onExitItems)

                if(verifySuccess):
                    #navigate to next page
                    self.exitUI = ExitSuccess()
                    self.close()
                    self.exitUI.show()
                else:
                    self.timer.stop()

         # Toggle the visibility of the dots
        
        status = [self.circle1.isVisible(), self.circle2.isVisible(), self.circle3.isVisible()]
        #print(status)
        if(status[0] and status[2]):
            self.circle3.hide()
            self.circle2.hide()
            return
        
        if(status[0] and not status[1]):
            self.circle2.show()
            return

        if(status[0] and status[1] and not status[2]):
            self.circle3.show()
            self.setStyleSheet("background-color: #fff")
            return
        
    def verify(self, itemsEntry, itemsExit):
            if(len(itemsEntry) == 0 and len(itemsExit) == len(itemsEntry)):
                self.status.setText("NO ITEMS DETECTED ON CHECKIN \n VERIFICATION SUCCESSFULL")
                return True
            
            #making sure you entered with the same items
            for i in itemsExit:
                found = False
                for j in itemsEntry:
                    if(i==j):
                        found = True
            
                if(not found):
                    self.setStyleSheet("background-color: #ff8f80")
                    self.status.setStyleSheet("color:#000; font-weight:bold; font-family:Fredoka; font-size:10pt")
                    self.status.setText(f'[{str(i).split(".")[0].lower()}] not Found on you on entry. \nPOTENTIAL THEFT-RAISING ALERT')
                    return False
                

            #now check for individual backend algorithms
            self.status.setText("ITEMS RETRIEVED CHECKING COLOR DIFFERENCE")
            time.sleep(1)
            baseEntryDirectory = f'./../data/ObjectsDetected/{self.dateNow}/{self.intent[0]}/entry/'
            baseExitDirectory = f'./../data/ObjectsDetected/{self.dateNow}/{self.intent[0]}/exit/'
            
            for item in itemsExit:
                entryItem = baseEntryDirectory+item
                exitItem  = baseExitDirectory + item

                #color checker algorithm
                color = Algorithms.ssimChecker(Algorithms(), entryItem, exitItem)

                #if color is below a certain range, disagree
                print("color check = ", color)
                if(color <= 0.6):
                    self.setStyleSheet("background-color: #fd7e14")
                    self.status.setStyleSheet("color:#000; font-weight:bold; font-family:Fredoka; font-size:10pt")
                    self.status.setText(f'COLOR CHECK FOR DEVICE [{str(i).split(".")[0].lower()}] FAILED \nPOTENTIAL THEFT-RAISING ALERT')
                    return False
                    
                #check for sift
                sift = Algorithms.ssimChecker(Algorithms(), entryItem, exitItem)
                print("sift = ", sift)
                if(sift <= 0.6):
                    self.setStyleSheet("background-color: #fd7e14")
                    self.status.setStyleSheet("color:#000; font-weight:bold; font-family:Fredoka; font-size:10pt")
                    self.status.setText(f'DEVICE MATCHING FOR [{str(i).split(".")[0].lower()}] FAILED \nPOTENTIAL THEFT-RAISING ALERT')
                    return False

            return True
    

    def retrieveItems(self, entryExitFlag):
        #retrieve exit items in db
        entryDb = db.queryDb(db(), self.intent[0], entryExitFlag)

        #making sure the data exists in the database
        if(len(entryDb)==0):
            return []

        #read the main items
        entryItems = entryDb[0][3:11]
        entryItems = [item for item in entryItems if item!=None]

        return entryItems


# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# app = QApplication(sys.argv)
# window = UI()

# app.exec_()