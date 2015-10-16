import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import time
import hardware
import random

def TakeScreenshot():
    if iswindows:
        WindowsScreenShot(filename)
    else:
        RaspPiScreenShot(filename)

def RaspPiScreenShot(filename):
    ## http://www.raspberrypi-spy.co.uk/2014/05/how-to-capture-minecraft-screenshots-on-the-raspberry-pi/
    pass

def WindowsScreenShot(filename):
    from PIL import ImageGrab
    import win32gui

    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
    # just grab the hwnd for first window matching firefox
    firefox = firefox[0]
    hwnd = firefox[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    img.show()


def Connect():
    connectToLocalServer = True

    if connectToLocalServer:
        return minecraft.Minecraft.create()
    else:
        # Server on my Raspberry Pi 2
        address = "192.168.0.13"
        port = 25565

        print("connecting to {}:{}".format(address, port))
        return minecraft.Minecraft.create(address,port)

def Rain(mc, duration, intensity, area, blockType):

    wait = 1 / intensity

    for t in range(duration):
        for i in range(intensity):

            x = random.randint(0 - area, 0 + area)
            y = 0 + 40
            z = random.randint(0 - area, 0 + area)

            s = "RAINING {} {} {} ".format(x, y, z)
            print(s)
            mc.postToChat(s)
            mc.setBlock(x,y,z,blockType)

            time.sleep(wait)
         


if __name__ == "__main__":
    mc = Connect()

    for n in range(3):
        Rain(mc, duration = 3, intensity = 3, area = 20, blockType = block.TNT)
        time.sleep(2)
    


    
    
 