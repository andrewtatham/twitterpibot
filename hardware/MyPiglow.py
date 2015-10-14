import math
import time
import random
from piglow import PiGlow

t = 0;
maxbright = 255
piglow = PiGlow()
piglow.all(0)
buffer = [0 for led in range(18)]

def getLed(arm, colour):
    return int(6 * arm + colour)

def getBright(factor):
    return max(0, min(int(-0.5 * maxbright + maxbright * factor),255))


def OnInboxItemRecieved(inboxItem):
    led = random.randint(0,17)
    buffer[led] = max(0, min((buffer[led] + 1), 255))
    WriteLed(led)

def Fade():
    for led in range(18):
        if buffer[led] > 1:
            buffer[led] = max(0,buffer[led] - 5)        
    WriteAll()

def WriteAll():
    for led in range(18):
        args.WriteLed(led)

def WriteLed( led):
    bright = max(0, min(buffer[led], 255))
    args.piglow.led(led + 1, bright)

def CameraFlash( on):
    if on:
        piglow.white(255)
    else:
        WriteAll()

def Close(args):    
    piglow = None