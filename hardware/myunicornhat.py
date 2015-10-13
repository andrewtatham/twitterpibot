import random
import unicornhat


buffer = [[(0,0,0) for x in range(8)] for y in range(8)]

class MyUnicornHat(object):

    def CameraFlash(args, on):
        for y in range(8):
            for x in range(8):
                if on:
                    r = 255
                    g = 255
                    b = 255
                else:
                    pixel = buffer[x][y]
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()

    def OnInboxItemRecieved(args, inboxItem):
        x = random.randint(0,7)
        y = random.randint(0,7)
        r = random.randint(1,255)
        g = random.randint(1,255)
        b = random.randint(1,255)
        buffer[x][y] = (r,g,b)
        unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()

    def Fade(args):
        for y in range(8):
            for x in range(8):
                pixel = buffer[x][y]
                r = max(pixel[0] - 1, 0)
                g = max(pixel[1] - 1, 0)
                b = max(pixel[2] - 1, 0)
                buffer[x][y] = (r,g,b)
                unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()

    def Close(args):
        r = 0
        g = 0
        b = 0
        for y in range(8):
            for x in range(8):
                unicornhat.set_pixel(x,y,r,g,b)
        unicornhat.show()
