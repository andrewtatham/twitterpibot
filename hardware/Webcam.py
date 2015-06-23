from Camera import *
from ExceptionHandler import ExceptionHandler

enableWebcam = False
try:
    import cv2
    import urllib
    import numpy as np
except Exception as e:
    ExceptionHandler().HandleSilently(e)

    enableWebcam = False


class Webcam(Camera):
    def __init__(self, *args, **kwargs):

        try:

            self.webcam = cv2.VideoCapture(args[0])
            #cv2.namedWindow("webcam" + str(args[0]))
            for i in range(5):
                err,image = self.webcam.read()
            self.enabled = True

        except Exception as e:
            ExceptionHandler().HandleSilently(e)
            self.enabled = False
            



    def TakePhoto(args):
        if args.enabled:
            photo = WebcamPhoto()
            for i in range(5):
                err,image = args.webcam.read()
            photo.image = image                      
            return photo

        else:
            return None


    def Close(args):
        args.webcam.release()



class WebcamPhoto(Photo):
    pass