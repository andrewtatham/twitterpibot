import random
import unicornhat

class MyUnicornHat(object):

    def CameraFlash(args, on):

        r = 0
        g = 0
        b = 0
        if on:
            r = 255
            g = 255
            b = 255

        for y in range(8):
            for x in range(8):
                unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()



    def OnInboxItemRecieved(args, inboxItem):
        x = random.randint(0,7)
        y = random.randint(0,7)
        r = random.randint(1,255)
        g = random.randint(1,255)
        b = random.randint(1,255)
        unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()

    def Fade(args):
        pass

    def Close(args):
        r = 0
        g = 0
        b = 0
        for y in range(8):
            for x in range(8):
                unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()
