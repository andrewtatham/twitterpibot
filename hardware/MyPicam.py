
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
            self.enabled = True

    def TakePhoto(args):
        with args.lock:
            print('taking photo')
            
            args.mypicamera.capture(args.picamerastream, format='rgb')

            photo = MyPicamPhoto()
            args.picamerastream.truncate(0)
            photo.image = args.picamerastream.array
            args.picamerastream.truncate(0)
            return photo


    def TakePhotoToDisk(args, dir, name, ext, nightmode = False):
        with args.lock:
            filename = dir + os.path.sep + name + os.extsep + ext

            if nightmode:
                # Set a framerate of 1/6fps, then set shutter
                # speed to 6s and ISO to 800
                args.mypicamera.framerate = Fraction(1, 6)
                args.mypicamera.shutter_speed = 6000000
                args.mypicamera.exposure_mode = 'off'
                args.mypicamera.iso = 800
                # Give the camera a good long time to measure AWB
                # (you may wish to use fixed AWB instead)
                time.sleep(10)

            args.mypicamera.capture(filename)
            return filename



    def Close(args):
        with args.lock:
            args.mypicamera.close()
            args.picamerastream.close()
            # cv2.namedWindow("picamera")

class MyPicamPhoto(Photo):
    pass