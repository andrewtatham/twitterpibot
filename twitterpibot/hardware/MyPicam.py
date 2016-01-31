import os

import picamera
import picamera.array


def take_photo(folder, name, ext):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    filename = folder + os.path.sep + name + os.extsep + ext
    camera.capture(filename)
    camera.close()
    return filename
