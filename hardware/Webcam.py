from Camera import *
from ExceptionHandler import HandleSilently
import os
import threading
import cv2
import urllib
import numpy as np

class Webcam(Camera):
    def __init__(self, *args, **kwargs):        
        self.lock = threading.Lock()
        self.webcam = cv2.VideoCapture(args[0])
        for i in range(5):
            err,image = self.webcam.read()

    def TakePhoto(args):
        with args.lock:
            photo = WebcamPhoto()
            for i in range(5):
                err,image = args.webcam.read()
            photo.image = image                      
        return photo


    def TakePhotoToDisk(args, dir, name, ext, nightmode):
        with args.lock:
            for i in range(5):
                err,image = args.webcam.read()
            filename = dir + os.path.sep + name + os.extsep + ext
            cv2.imwrite(filename, image)
        return filename

    def Close(args):
        with args.lock:
            args.webcam.release()

class WebcamPhoto(Photo):
    pass