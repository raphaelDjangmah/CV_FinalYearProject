from Action import UI as AppStart
from AdminHome import UI as StartAdmin
from PyQt5.QtWidgets import *
import sys,os


if __name__ == '__main__':
    
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication([])
    
    window = AppStart()
    window.show()

    admin = StartAdmin()
    admin.show()
    print("APPLICATION STARTED...")
    app.exec_()
    
    # status = int(input('Press 1 to ENTER and Press 0 to EXIT : '))

    # if(status != 0 and status != 1):
    #     print('Invalid Input')
    #     exit()
    
    # #take student ID 
    # studentID = int(input('Input Your Student ID : '))
    
    # #take picture
    # photo = Model.TakePhoto()
    # photo.take(studentID, status)

    # #extract 
    # objects = Model.ExtractObjects()
    # objects.extract(studentID, status)


    # #if exit, check Exit properties
    # if(status == 0):
    #     exit = ModelExit.CheckExit()
    #     exitter = exit.exitter(studentID)
        
    #     if(exit.getCode() != 1):
    #         #raise alert
    #         print("EXIT CHECK FAILED!")
    #         print("REASON = ", exit.getMessage())
    #         pass
    #     else:
    #         print("CHECK COMPLETED. YOU ARE GOOD TO GO")
        