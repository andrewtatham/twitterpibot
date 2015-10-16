import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import time
import hardware

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
    if hardware.iswindows:
        return minecraft.Minecraft.create( server.address )
    else:
        return minecraft.Minecraft.create()

     


if __name__ == "__main__":



    mymc = MyMineCraft()


    mymc.foo()