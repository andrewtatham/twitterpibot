import os
# noinspection PyPackageRequirements
import cv2

camera = cv2.VideoCapture(0)


def take_photo(folder, name, ext):
    for i in range(5):
        camera.read()
    err, image = camera.read()
    filename = folder + os.path.sep + name + os.extsep + ext
    cv2.imwrite(filename, image)
    return filename


def close():
    camera.release()
