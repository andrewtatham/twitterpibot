import os
import threading
import picamera
import picamera.array


class MyPicam(object):
    def __init__(self):
        self.lock = threading.Lock()

        with self.lock:
            self.mypicamera = picamera.PiCamera()
            self.mypicamera.resolution = (320, 240)

    def TakePhotoToDisk(self, dir, name, ext):
        with self.lock:
            filename = dir + os.path.sep + name + os.extsep + ext
            self.mypicamera.capture(filename)
            return filename

    def close(self):
        with self.lock:
            self.mypicamera.close()
