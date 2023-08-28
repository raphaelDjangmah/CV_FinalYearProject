from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys,os

class UI(QFrame):
    def __init__(self):
        super(UI, self).__init__()

        #load ui File
        uic.loadUi('./../designs/AdminAccessControl.ui', self)
        self.setWindowTitle("BALME SSH")
        self.show()

        #identify widget
        self.table      = self.findChild(QTableWidget, "tb_student_access")
        self.addId      = self.findChild(QPushButton, "add_student")
        
        self.addId.clicked.connect(self.addRestriction)
        
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,80)
        self.loadData()

    
    def addRestriction(self):
        #get the text from the editfield and fill
        inputId = self.findChild(QLineEdit, "input_res_id")
        
        with open('./../data/restrictedUsers.csv', 'a+') as f:
            fileData = f.write("\n"+inputId.text())
        
        inputId.setText("")
        self.loadData()

    def grantAccess(self):
        sender = self.sender()
        button_name = sender.objectName()

        print(button_name)
        
        #read the csv and remove that id
        with open('./../data/restrictedUsers.csv', 'r') as f:
            fileData = f.read()
        
        fileData = fileData.replace(button_name,"")
        
        with open('./../data/restrictedUsers.csv', 'w') as f:
            f.write(fileData)

        self.loadData()

    def loadData(self):
        with open('./../data/restrictedUsers.csv', 'r') as f:
            fileData = f.read()
        
        restricted = fileData.split('\n')
        restricted = [res for res in restricted if res!=""]
        self.table.setRowCount(len(restricted))
        rows = 0

        for data in restricted:
            widget = QWidget()  # Create a widget to hold the button
            layout = QHBoxLayout()  # Create a layout to hold the button
            button = QPushButton("Grant Access")
            button.setObjectName(str(data))
            button.setFixedWidth(50)
            button.setFixedHeight(20)
            button.setStyleSheet("border: None;\n"   
                            "font-family: Fredoka;\n"
                            "font-size: 5pt;\n"
                            "font-weight:bold;\n"
                            "border: 1px solid #000;\n"
                            "border-radius: 5px;\n"
                            "background-color:red;\n"
                            "color: #fff;"
                )
            
            button.clicked.connect(self.grantAccess)
            layout.addWidget(button)
            widget.setLayout(layout)
            
            self.table.setItem(rows, 0, QTableWidgetItem(data))
            self.table.setCellWidget(rows, 1, widget)  # Set the widget with the button in the cell
            rows += 1
#--
if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication([])
    
    window = UI()
    window.show()
    app.exec_()