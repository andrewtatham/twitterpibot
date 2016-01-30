import os
# noinspection PyPackageRequirements
import cv2


class Webcam(object):
    def __init__(self):
        self._webcam = cv2.VideoCapture(0)
        for i in range(5):
            self._webcam.read()

    def TakePhotoToDisk(self, dir, name, ext):
        for i in range(5):
            self._webcam.read()
        err, image = self._webcam.read()
        filename = dir + os.path.sep + name + os.extsep + ext
        cv2.imwrite(filename, image)
        return filename

    def close(self):
        self._webcam.release()
