import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import time

class MyMineCraft(object):




    def foo(args):

        if iswindows:
            mc = minecraft.Minecraft.create( server.address )
        else:
            mc = minecraft.Minecraft.create()






        mc.postToChat("x")
        for x in range(1,8):
            mc.setBlock(x,0,0, block.SANDSTONE)
        mc.postToChat("y")
        for y in range(1,8):
            mc.setBlock(0, y, 0, block.GRAVEL)
        mc.postToChat("z")
        for z in range(1,8):
            mc.setBlock(0,0,z, block.WOOD)


        mc.setBlock(0,0,0, block.TNT, 1)


        # position player/camera
        mc.player.setPos(8, 0, 8)
        
        
        iswindows = True

        filename = "temp.png"

        # take screenshot
        if iswindows:
            WindowsScreenShot(filename)
        else:
            RaspPiScreenShot(filename)


        mc.postToChat("done")

        return filename

    def RaspPiScreenShot(args, filename):
        ## http://www.raspberrypi-spy.co.uk/2014/05/how-to-capture-minecraft-screenshots-on-the-raspberry-pi/
        pass

    def WindowsScreenShot(args, filename):


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
      


if __name__ == "__main__":



    mymc = MyMineCraft()


    mymc.foo()