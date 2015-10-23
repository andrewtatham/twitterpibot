import random
import unicornhat
import time
import itertools
from multiprocessing import Lock


def _WritePixel(x, y):
    pixel = _buffer[x][y]
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    unicornhat.set_pixel(x,y,r,g,b)

def _WriteAll():
    for y in range(8):
        for x in range(8):
            _WritePixel(x, y)
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




class RainMode(UnicornHatMode):

    def __init__(self):
        self._rain = Rain()
  

    def Lights(self):
        with _lock:
            self._rain.WriteToBuffer()
            _WriteAll()
            self._rain.Iterate()
        time.sleep(2)

    def OnInboxItemRecieved(self, inboxItem):
        rgb = (0,0,255)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer()
        _WriteAll()



class Rain(object):
    def __init__(self, direction = "down"):
        self._direction = direction
        self._raindrops = []


    def AddRaindrop(self, rgb):
        if self._direction == "down":
            x = random.randint(0,7)
            y = 7
        self._raindrops.add(Raindrop(x,y,rgb))

    def WriteToBuffer(self):
        for r in self._raindrops:
            _buffer[r._x][r._y] = r._rgb

    def Iterate(self):
        for r in self._raindrops:
            if direction == "down":
                r._y -= 1
                if r.y < 0:
                    self._raindrops.remove(r)

class Raindrop(object):
    def __init__(self, x, y, rgb):
        self._x = x
        self._y = y
        self._rgb = rgb

            


_buffer = [[(0,0,0) for x in range(8)] for y in range(8)]
_modes = itertools.cycle([
    #DotsMode(),
    #FlashMode(),
    RainMode()


    #TODO
    # Rain
    # matrix
    # Fire
    # bubbles
    #Fireworks
    # Sin Wave
    # Swipes
    # graphic equalizer
    # starfield
    
    # bouncing ball/line

    # snake
    # game of life
    # battleships
    # chess/draughts

    # strobe
    # lifts?
    # text/numbers
    # emoticons
    # graphs
    # random/noise
    # images / video / gifs
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
        global _mode
        _mode = next(_modes)

def Fade():
    _mode.Fade();

def Close():
    _mode.Close()








    