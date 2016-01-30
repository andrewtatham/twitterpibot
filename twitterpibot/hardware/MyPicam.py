import os

import picamera
import picamera.array


class MyPicam(object):
    def __init__(self):
        self.mypicamera = picamera.PiCamera()
        self.mypicamera.resolution = (640, 480)

    def TakePhotoToDisk(self, dir, name, ext):
        filename = dir + os.path.sep + name + os.extsep + ext
        self.mypicamera.capture(filename)
        return filename

    def close(self):
        self.mypicamera.close()
