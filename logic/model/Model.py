from ultralytics import YOLO
import cv2
import cvzone
import math
from .YoloObjects import Objects
import time
from datetime import datetime
import os
from .Utilities import Databases as util


class TakePhoto:
    def take(self, studentID, entryOrExit = True):
        imageTaken = False 
        startTime, prevTime   = None, None

        #load a nano version of the weights
        model = YOLO('./../yolo-weights/yolov8n.pt')

        #open the webcam size 640x480
        webcam = cv2.VideoCapture(0)
        webcam.set(3, 720)
        webcam.set(4, 640)

        while imageTaken == False:
            success, image = webcam.read()
            results = model(image, stream=True)

            #loop thru each stream
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    
                    #bounding box using fancy rectangle
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    w, h =  x2-x1, y2-y1

                    #confidence 
                    conf = (math.ceil((box.conf[0]*100))/100)*100

                    #class name
                    cls = box.cls[0]

                    #if there is a human in the photo with 70% confidence, save it
                    # if(Objects.getClassname(Objects, int(cls)) == 'person' and conf>=70):
                    if(True):
                        waitTimeInSec = 10
                        
                        if(startTime == None):
                            print("GET READY TO TAKE PHOTO... wait time = ", waitTimeInSec," seconds")
                            startTime = time.time()
                        else:
                            if(int(time.time() - startTime) >= waitTimeInSec):
                                timestamp = datetime.now()
                                
                                entryExitTag = ""
                                if(entryOrExit):
                                    entryExitTag = "entry"
                                else:
                                    entryExitTag = "exit"

                                directory = f'./../data/ObjectsDetected/{timestamp.date()}/{studentID}/{entryExitTag}/'
                                os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
                                filename = 'fullImage.png'
                                path = os.path.join(directory, filename)


                                cv2.imwrite(path, image)
                                print("PICTURE TAKEN SUCCESSFULLY")
                                imageTaken = True
                            else:
                                if(int(time.time() - startTime)!=prevTime):
                                    cvzone.putTextRect(image, f'Ready : {prevTime}/{waitTimeInSec}', (max(0,x1),max(35, y1-20)), scale=1)
                                    prevTime = int(time.time() - startTime)
                                    print("GET READY...", prevTime+1)

                    else:
                        print("could not identify you look directly into the camera") 
                    
                if imageTaken:
                    webcam.release()
                    cv2.destroyAllWindows()

            #close the webcam
            cv2.imshow("Image", image)
            cv2.waitKey(1)


class ExtractObjects:
    def extract(self, studentID, entryOrExit = True):
        timestamp = datetime.now()
        entryExitTag = ""

        if(entryOrExit):
            entryExitTag = "entry"
        else:
            entryExitTag = "exit"

        directory = f'./../data/ObjectsDetected/{timestamp.date()}/{studentID}/{entryExitTag}/'
        # directory = f'./../../data/ObjectsDetected/{timestamp.date()}/{studentID}/{entryExitTag}/'
        objCounts = 0

        #save the user to db for the firsttime
        util.saveToDb(util() , studentID, None, entryOrExit)

        #use larger weight for better detection
        image = cv2.imread(f'{directory}fullImage.png')

        #image processing
        # resized_image = cv2.resize(image, (520,520))    #resizing image to size of model
        # normalized_image = resized_image/255.0
        # image = normalized_image

        model = YOLO('./../yolo-weights/LaptopDetector.pt')
        result = model(image)
        objCounts = 0

        #creata a dummy person
        os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
        filename = 'person.png'
        path = os.path.join(directory, filename)
        cv2.imwrite(path, image)

        #show result
        for r in result:
            boxes = r.boxes
            for box in boxes:
                
                #bounding box using fancy rectangle
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                w, h =  x2-x1, y2-y1

                #confidence 
                classname = ['laptop']
                cls  = int(box.cls[0])
                conf = (math.ceil((box.conf[0]*100))/100)*100
                imType = classname[cls]
                print(f'{imType} score = {conf}')
                

                #if a higher accuracy is found, detect the exact type of laptop
                if(conf >= 60):   

                    print("CONFIDENCE = ", conf) 

                    #class name
                    cvzone.cornerRect(image, (x1, y1, w, h))
                    cvzone.putTextRect(image, imType, (max(0,x1),max(35, y1-20)), scale=1)

                    #get the exact class of laptop
                    laptopModel         = YOLO('./../yolo-weights/LaptopTypeDetector.pt')
                    laptopTypeClasses   = ['Hp','MacBook','Dell','Lenovo']           
                    laptopTypeModel     = laptopModel(image)
                    laptopName          = 'Laptop'
                    laptopType          = "undefined"
                    objCounts+=1

                    for z in laptopTypeModel:
                        boxes_ = z.boxes

                        for box_ in boxes_:
                            #bounding box using fancy rectangle
                            a1, b1, a2, b2 = box_.xyxy[0]
                            a1, b1, a2, b2 = int(a1), int(b1), int(a2), int(b2)
                            
                            w, h =  a2-a1, b2-b1

                            #confidence 
                            cls_    = int(box_.cls[0])
                            conf_   = (math.ceil((box_.conf[0]*100))/100)*100
                            imgType = laptopTypeClasses[cls_]
                            print(f'{imgType} score = {conf_}')
                            

                            #if a higher accuracy is found, detect the exact type
                            if(conf_ > 20):    
                                #class name
                                # cvzone.cornerRect(image, (x1, y1, w, h))
                                # cvzone.putTextRect(image, imType, (max(0,x1),max(35, y1-20)), scale=1)

                                # os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
                                # filename = laptopTypeName+'-'+imType
                                # path = os.path.join(directory, filename)
                                laptopType = imgType
                                break
                    
                    #save an image of the detected laptop to file
                    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
                    filename = f'{laptopName}-{laptopType}.png'
                    path = os.path.join(directory, filename)

                    cropped_image = image[y1:y2, x1:x2]
                    cv2.imwrite(path, cropped_image)

                    #save to the database
                    print("SAVING INTO DATABASE = ", util.updateDb(util(), studentID, objCounts, filename, entryOrExit))
                    print('Exiting')

        if(objCounts==0):
            print("NO DETECTED LAPTOPS ON YOU")
