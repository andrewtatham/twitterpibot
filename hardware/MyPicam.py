import os
import threading
import picamera
import picamera.array

class MyPicam(object):
    def __init__(self, *args, **kwargs):

        self.lock = threading.Lock()

        with self.lock:
            self.mypicamera = picamera.PiCamera()
            self.mypicamera.resolution = (320,240)


    def TakePhotoToDisk(args, dir, name, ext):
        with args.lock:
            filename = dir + os.path.sep + name + os.extsep + ext
            args.mypicamera.capture(filename)
            return filename

    def Close(args):
        with args.lock:
            args.mypicamera.close()


