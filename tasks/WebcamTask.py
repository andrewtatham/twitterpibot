
try:
    import cv2
    import urllib
    import numpy as np
except Exception:
    enableImages = False
    enableWebcam = False



def WebcamTasks():
    # INIT WEBCAM
    webcam = None
    if enableWebcam:
        webcam = cv2.VideoCapture(0)
        cv2.namedWindow("webcam")
        for i in range(5):
            err,frame = webcam.read()

    while running and enableWebcam:
        try:
            #print('Running WebcamTasks: %s' % time.ctime())
 
            err,image = webcam.read()           
            cv2.imshow("webcam", image)
            #cv2.waitKey(1)
            time.sleep(5)

        except Exception as e:
            logging.exception(e)             
            print(e)


    
if enableWebcam:
    webcam.release()
    cv2.namedWindow("webcam")
