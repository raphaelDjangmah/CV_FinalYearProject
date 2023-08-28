from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from datetime import datetime
import sys,os
from EntryDone import UI as ExitUI
from model.Utilities import Databases as db;
# from AwaitCam import UI as AwaitCame
from model.Model import TakePhoto as WebCam
import cv2

class UI(QFrame): 
    def __init__(self, data):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/ItemConfirm.ui', self)
        
        #get data
        self.intent = data

        #identify widget
        self.table      = self.findChild(QTableWidget, "tb_confirm_items")
        self.confirmBtn = self.findChild(QPushButton, "objects_accept")
        self.rejectBtn  = self.findChild(QPushButton, "objects_reject")

        self.confirmBtn.clicked.connect(self.confirmAccurate)
        self.rejectBtn.clicked.connect(self.rejectAccurate)

        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,150)

        self.acceptUI = ExitUI()
        
        #load data into the table / ---- will be gotten from the database
        self.loadData()

        #
        # self.setWindowTitle("BALME SSH")
        # self.show()

    def confirmAccurate(self):
        #navigate back to webcam page
        self.close()
        self.acceptUI.show()

    def rejectAccurate(self):
        return
        #navigate to the webcam loading screen
        self.close()  
        self.camWaitUI = AwaitCame(self.intent)
        self.camWaitUI.show()

        #continue to finish page-------------------
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)

        #open webcam
        WebCam.take(WebCam(), self.intent[0], self.intent[1])

        # Close the main application window
        cv2.destroyAllWindows()


    def loadData(self):
        items = self.retrieveItems()
        self.dateNow = (datetime.now()).date()
        self.directory = f'./../data/ObjectsDetected/{self.dateNow}/{self.intent[0]}/entry/'

        extractedResult = []
        row = 0
        for item in items:
            image = self.directory + item
            deviceName = (item.split('.'))[0]
            extractedResult.append({"Device Name":deviceName, "Captured Image":image})


        self.table.setRowCount(len(extractedResult))
        for result in extractedResult:
            self.table.setItem(row, 0, QTableWidgetItem(result['Device Name']))

            # Create a QTableWidgetItem with an icon
            image_item = QTableWidgetItem()
            image_path = result['Captured Image']
            icon = QIcon(image_path)

            # Set the desired icon size
            icon_size = QSize(64, 64)  # Adjust the size as needed
            icon = icon.pixmap(icon_size)
            image_item.setIcon(QIcon(icon))

            # Set the icon to the cell
            self.table.setItem(row, 1, image_item)

            # Resize the cell to fit the image
            self.table.setRowHeight(row, icon_size.height())
            self.table.setIconSize(icon_size)  # Set the icon size

            row+=1

    def retrieveItems(self):
        #retrieve exit items in db
        entryDb = db.queryDb(db(), self.intent[0], self.intent[1])

        #making sure the data exists in the database
        if(len(entryDb)==0):
            return []

        #read the main items
        entryItems = entryDb[0][3:11]
        entryItems = [item for item in entryItems if item!=None]

        return entryItems


# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# app = QApplication(sys.argv)
# window = UI([10022, 1])

# app.exec_()