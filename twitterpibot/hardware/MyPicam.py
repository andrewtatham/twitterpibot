import os

import picamera.array

camera = picamera.PiCamera()
camera.resolution = (640, 480)


def take_photo(folder, name, ext):
    filename = folder + os.path.sep + name + os.extsep + ext
    camera.capture(filename)
    return filename


def close():
    camera.close()
