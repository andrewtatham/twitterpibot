
from Camera import Camera, Photo
import time
from ExceptionHandler import ExceptionHandler
import cv2
import os
import threading


try:
    import picamera
    import picamera.array

except Exception as e:
    ExceptionHandler().HandleSilently(e)

  


class MyPicam(Camera):
    def __init__(self, *args, **kwargs):

        self.lock = threading.Lock()

        try:
            with self.lock:
                self.mypicamera = picamera.PiCamera()
                self.mypicamera.resolution = (640,480)
                self.picamerastream = picamera.array.PiRGBArray(self.mypicamera) 
                self.enabled = True

        except Exception as e:
            ExceptionHandler().HandleSilently(e)
            self.enabled = False
                
    
    


    def TakePhoto(args):
        if args.enabled:
            with args.lock:
                print('taking photo')
            
                args.mypicamera.capture(args.picamerastream, format='rgb')

                photo = MyPicamPhoto()
                args.picamerastream.truncate(0)
                photo.image = args.picamerastream.array
                args.picamerastream.truncate(0)
                return photo
        else:
            return None

    def TakePhotoToDisk(args, dir, name, ext):
        if args.enabled:
            
            with args.lock:
                filename = dir + os.path.sep + name + os.extsep + ext
                self.mypicamera.capture(filename)
                return filename

        else:
            return None


    def Close(args):
        if args.enabled:
            with args.lock:

                args.mypicamera.close()
                args.picamerastream.close()
                # cv2.namedWindow("picamera")

class MyPicamPhoto(Photo):
    pass