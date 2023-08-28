
import pixellib
import cv2
from pixellib.instance import instance_segmentation


segmentation_model = instance_segmentation()
segmentation_model.load_model('./../../Yolo-Weights/mask_rcnn_coco.h5')


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    #apply instance
    # res = segmentation_model.segmentFrame(frame, show)

    cv2.imshow('Capture Image', frame)

    # if(cv2.waitKey(10)):
    #     break

cap.release()
cv2.destroyAllWindows()


