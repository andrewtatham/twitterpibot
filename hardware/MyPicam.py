
from Camera import Camera, Photo
import time
from ExceptionHandler import HandleSilently
import cv2
import os
import threading
from fractions import Fraction
import picamera
import picamera.array

class MyPicam(Camera):
    def __init__(self, *args, **kwargs):

        self.lock = threading.Lock()

        with self.lock:
            self.mypicamera = picamera.PiCamera()
            self.mypicamera.resolution = (320,240)
            self.picamerastream = picamera.array.PiRGBArray(self.mypicamera) 


    def TakePhoto(args):
        with args.lock:
            print('taking photo')
            
            args.mypicamera.capture(args.picamerastream, format='rgb')

            photo = MyPicamPhoto()
            args.picamerastream.truncate(0)
            photo.image = args.picamerastream.array
            args.picamerastream.truncate(0)
            return photo


    def TakePhotoToDisk(args, dir, name, ext):
        with args.lock:
            filename = dir + os.path.sep + name + os.extsep + ext
            args.mypicamera.capture(filename)
            return filename



    def Close(args):
        with args.lock:
            args.mypicamera.close()
            args.picamerastream.close()


class MyPicamPhoto(Photo):
    pass