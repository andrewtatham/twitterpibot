import random
import unicornhat
import time
import itertools
from multiprocessing import Lock


def _WritePixel(self, x, y):
    pixel = _buffer[x][y]
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    unicornhat.set_pixel(x,y,r,g,b)

def _WriteAll(self):
    for y in range(8):
        for x in range(8):
            self._WritePixel(x, y)
    unicornhat.show()

class UnicornHatMode(object):

    def CameraFlash(self, on):
        with _lock:
            for y in range(8):
                for x in range(8):
                    if on:
                        r = 255
                        g = 255
                        b = 255
                    else:
                        pixel = _buffer[x][y]
                        r = pixel[0]
                        g = pixel[1]
                        b = pixel[2]
                    unicornhat.set_pixel(x,y,r,g,b)
            unicornhat.show()

    def Fade(self):
        with _lock:
            for y in range(8):
                for x in range(8):
                    pixel = _buffer[x][y]
                    r = max(pixel[0] - 1, 0)
                    g = max(pixel[1] - 1, 0)
                    b = max(pixel[2] - 1, 0)
                    _buffer[x][y] = (r,g,b)
                    unicornhat.set_pixel(x,y,r,g,b)
            unicornhat.show()

    def Close(self):
        with _lock:
            r = 0
            g = 0
            b = 0
            for y in range(8):
                for x in range(8):
                    unicornhat.set_pixel(x,y,r,g,b)
            unicornhat.show()

class DotsMode(UnicornHatMode):


    def Lights(self):
        with _lock:
            x = random.randint(0,7)
            y = random.randint(0,7)
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
            _buffer[x][y] = (r,g,b)
            unicornhat.set_pixel(x,y,r,g,b)
            unicornhat.show()
        time.sleep(2)

    def OnInboxItemRecieved(self, inboxItem):
        with _lock:
            x = random.randint(0,7)
            y = random.randint(0,7)
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
            _buffer[x][y] = (r,g,b)
            unicornhat.set_pixel(x,y,r,g,b)
            unicornhat.show()

class FlashMode(UnicornHatMode):
    


    def Lights(self):

        with _lock:
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = (r,g,b)
            _WriteAll()
        time.sleep(2)

    def OnInboxItemRecieved(self, inboxItem):
        with _lock:
            r = random.randint(1,255)
            g = random.randint(1,255)
            b = random.randint(1,255)
            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = (r,g,b)
            _WriteAll()


_buffer = [[(0,0,0) for x in range(8)] for y in range(8)]
_modes = itertools.cycle([
    DotsMode(),
    FlashMode()
    ])
_mode = next(_modes)

_lock = Lock()

def Lights():
    _mode.Lights()

def CameraFlash(on):
    _mode.CameraFlash(on)

def OnInboxItemRecieved(inboxItem):
    _mode.OnInboxItemRecieved(inboxItem)

def OnLightsScheduledTask():
    with _lock:
        _mode = next(_modes)

def Fade():
    _mode.Fade();

def Close():
    _mode.Close()








    