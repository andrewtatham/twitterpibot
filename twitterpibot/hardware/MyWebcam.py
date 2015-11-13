import os
import threading
# noinspection PyPackageRequirements
import cv2


class Webcam(object):
    def __init__(self):
        self._lock = threading.Lock()
        with self._lock:
            self._webcam = cv2.VideoCapture(0)
            for i in range(5):
                self._webcam.read()

    def TakePhotoToDisk(self, dir, name, ext):
        with self._lock:
            for i in range(5):
                self._webcam.read()
            err, image = self._webcam.read()
            filename = dir + os.path.sep + name + os.extsep + ext
            cv2.imwrite(filename, image)
        return filename

    def close(self):
        with self._lock:
            self._webcam.release()
