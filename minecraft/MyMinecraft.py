import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import time
import hardware
import random


def ArrangeScreenshot(mc):
    pass



def TakeScreenshot(filename):
    if hardware.iswindows:
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
        

def Pyramid(mc, x, z, height):
    for y in range(height):
        
        n = (height - y) - 1
        
        s = "PYRAMID {} {} ".format(y, n)
        print(s)
        mc.postToChat(s)

        mc.setBlocks(x-n, y, z-n, x+n, y, z+n, block.TNT, 1)
        




def Clear():
    mc.setBlocks(-100,0,-100,100,100,100, block.AIR)

if __name__ == "__main__":
    mc = Connect()
 


    Clear()

    Pyramid(mc, 0, 0, 10)


    Rain(mc, duration = 3, intensity = 3, area = 20, blockType = block.LAVA_FLOWING)
    

    #ids = mc.getPlayerEntityIds()
    #for id in ids:
    #    print(id)


    #pos = mc.player.getTilePos()

    #print(pos.x,pos.y,pos.z)
    #ArrangeScreenshot(mc)
    #TakeScreenshot("temp/mc.png")

    time.sleep(10)

   
    
 