from Camera import *
from ExceptionHandler import ExceptionHandler
import os
import threading

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
        
        self.lock = threading.Lock()

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
            with args.lock:
                photo = WebcamPhoto()
                for i in range(5):
                    err,image = args.webcam.read()
                photo.image = image                      
            return photo

        else:
            return None

    def TakePhotoToDisk(args, dir, name, ext):
        if args.enabled:
            with args.lock:

                for i in range(5):
                    err,image = args.webcam.read()
                filename = dir + os.path.sep + name + os.extsep + ext
                cv2.imwrite(filename, image)
                         
            return filename

        else:
            return None

    def Close(args):
        with args.lock:
            args.webcam.release()



class WebcamPhoto(Photo):
    pass