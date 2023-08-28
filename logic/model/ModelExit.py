
from datetime import datetime
import Utilities as util
import cv2
import PictureAlgorithms as algos
import os

class CheckExit:

    #
    message = ''
    code = 0

    def getMessage(self):
        return self.message
    def getCode(self):
        return self.code
    def setMessage(self, mes):
        self.message = mes
    def setcode(self, cod):
        self.code = cod


    #---------------------------------------------------------------------
    def exitter(self, studentID):

        db = util.Databases()

        #retrieve exit items in db
        exitDb  = db.queryDb(studentID, 0)
        entryDb = db.queryDb(studentID, 1)

        #making sure the data exists in the database
        if(len(exitDb) ==0  or len(entryDb)==0):
            self.setcode(0)
            self.setMessage('FATAL ERR: Could not find any record of you on entry')
            return

        #read the main items
        date       = (exitDb[0][13]).date()
        exitItems  = exitDb[0][3:11]
        exitItems  = [item for item in exitItems if item!=None]
        entryItems = entryDb[0][3:11]
        entryItems = [item for item in entryItems if item!=None]

        #no device on entry or exit
        if(len(exitItems) == 0 and len(exitItems) == len(entryItems)):
            self.setcode(1)
            self.setMessage('No devices checked in and out with')
            return

        #make sure all entry and exit items match
        for i in exitItems:
            found = False
            for j in entryItems:
                if(i==j):
                    found = True
            
            if(not found):
                self.setcode(-1)
                self.setMessage(f'[{i}] not Found on you on entry')
                return
        

        #loop thru each item for both entry and exit
        pathEntry = f'../../data/ObjectsDetected/{date}/{studentID}/entry/'
        pathExit  = f'../../data/ObjectsDetected/{date}/{studentID}/exit/'
        algorithms = algos.Algorithms()

        for img in exitItems:
            imageEntry = pathEntry+img
            imageExit  = pathExit + img

            #making sure the file exits
            if(not os.path.isfile(imageEntry) or not os.path.isfile(imageEntry)):
                self.setMessage(f'FILE {img} DOES NOT EXIST')
                self.setcode(-1)
                return

            #pass thru all algo checks
            ssimChecker = algorithms.ssimChecker(imageEntry, imageExit)
            if(ssimChecker < 0.7):
                self.setMessage(f'COLOR THRESHOLD for {img} FAILED TO PASS = {ssimChecker}')
                self.setcode(-1)
                return 
            
            print(f"COLOR CHECKER PASSED SUCCESSFULLY FOR DEVICE = {img} {ssimChecker}")

            #print passes
        
        if(len(entryItems)>len(exitItems)):
            print("ITEMS ENTERED WITH ARE MORE THAN YOU ARE EXITING WITH. \nPLEASE REPORT TO SECURITY IF THIS IS A PROBLEM")

        self.setMessage(f'\nYOU HAVE BEEN CLEARED FOR EXIT. THANK YOU FOR USING BALME LIBRARY')
        self.setcode(1)

                

if __name__ == '__main__':
    check = CheckExit()
    check.exitter(10827454)
    print(check.getMessage())

