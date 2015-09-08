
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
                #self.mypicamera.start_preview()
                #time.sleep(2)
                #self.mypicamera.stop_preview()
                self.picamerastream = picamera.array.PiRGBArray(self.mypicamera) 
                #picamerawindow = cv2.namedWindow("picamera")
                self.enabled = True

        except Exception as e:
            ExceptionHandler().HandleSilently(e)
            self.enabled = False
                
    
    


    def TakePhoto(args):
        if args.enabled:
            with args.lock:
                print('taking photo')
            
                args.mypicamera.capture(args.picamerastream, format='grb')

                photo = MyPicamPhoto()
                args.picamerastream.truncate(0)
                photo.image = args.picamerastream.array
                #cv2.imshow("picamera", image)
                args.picamerastream.truncate(0)
                return photo
        else:
            return None

    def TakePhotoToDisk(args, dir, name, ext):
        if args.enabled:
            
            with args.lock:
                args.picamerastream.truncate(0)
                args.mypicamera.capture(args.picamerastream, format='grb')
                image = args.picamerastream.array
                args.picamerastream.truncate(0)

                filename = dir + os.path.sep + name + os.extsep + ext
                cv2.imwrite(filename, image)
                         
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