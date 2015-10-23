import random
import unicornhat
import time
import itertools
from multiprocessing import Lock

class UnicornHatMode(object):
    def Lights(self):
        print("UnicornHatMode.Lights")
        time.sleep(3)

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
        return super(DotsMode, self).Lights()

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
            
            if random.randint(0,1) == 0:
                r = random.randint(1,255)
                g = random.randint(1,255)
                b = random.randint(1,255)
            else:
                r = 0
                g = 0
                b = 0
            
            print("rgb = " + r + ", " + g + ", " + b)

            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = (r,g,b)

            for y in range(8):
                for x in range(8):
                    pixel = _buffer[x][y]
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                    unicornhat.set_pixel(x,y,r,g,b)
            unicornhat.show()
        super(DotsMode, self).Lights()

        time.sleep(0.25)


_buffer = [[(0,0,0) for x in range(8)] for y in range(8)]
_modes = itertools.cycle([
    DotsMode(),
    FlashMode()
    ])
_mode = next(_modes)
_lock = Lock()

def Lights():

    FlashMode.Lights(_mode)
    _mode.Lights()

def CameraFlash(on):
    _mode.CameraFlash(on)

def OnInboxItemRecieved(inboxItem):
    _mode.OnInboxItemRecieved(inboxItem)

def OnLightsScheduledTask():
    with _lock:
        _mode = next(_modes)
        print(_mode)

def Fade():
    _mode.Fade();

def Close():
    _mode.Close()








    