import os
import threading
import cv2

class Webcam(object):
    def __init__(self, *args, **kwargs):        
        self._lock = threading.Lock()
        with self._lock:
            self._webcam = cv2.VideoCapture(0)
            for i in range(5):
                err,image = self._webcam.read()

    def TakePhotoToDisk(args, dir, name, ext):
        with args._lock:
            for i in range(5):
                err,image = args._webcam.read()
            filename = dir + os.path.sep + name + os.extsep + ext
            cv2.imwrite(filename, image)
        return filename

    def Close(args):
        with args._lock:
            args._webcam.release()
