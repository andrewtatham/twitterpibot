import subprocess
import platform

ispiglowattached = False
ispicamattached = False
iswebcamattached = False
isbrightpiattached = False
isunicornhatattached = False

picam = None
webcam = None
brightpi = None

_platform = platform.platform()
print ("platform: " + _platform)
iswindows = _platform.startswith('Windows')
isRaspbian = not iswindows

_node = platform.node()
print ("node: " + _node)
isAndrewDesktop = _node == "ANDREWDESKTOP"
isAndrewLaptop = _node == "ANDREWLAPTOP"
isRaspberryPi = _node == "raspberrypi"
isRaspberryPi2 = _node == "raspberrypi2"

if iswindows:

    if isAndrewDesktop:
        iswebcamattached = False
    elif isAndrewLaptop:
        iswebcamattached = True

elif isRaspbian:

    test = subprocess.Popen(["sudo", "i2cdetect", "-y", "1"], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    print(str(output))

    if isRaspberryPi:
        iswebcamattached = True
        ispicamattached = False
        ispiglowattached = True  # bool(" 54 " in output)
        isbrightpiattached = bool(" 70 " in output)
    elif isRaspberryPi2:
        iswebcamattached = False
        isunicornhatattached = True

if iswebcamattached:
    import MyWebcam

    webcam = MyWebcam.Webcam()
if ispicamattached:
    import MyPicam

    picam = MyPicam.MyPicam()
if isunicornhatattached:
    import myunicornhat
if ispiglowattached:
    import MyPiglow
if isbrightpiattached:
    import MyBrightPi

    brightpi = MyBrightPi.BrightPI()


def TakePhotoToDisk(dir, name, ext, useFlash=False):
    try:
        if useFlash:
            CameraFlash(True)
        photos = []
        if iswebcamattached and webcam:
            photos.append(webcam.TakePhotoToDisk(dir, name, ext))
        if ispicamattached and picam:
            photos.append(picam.TakePhotoToDisk(dir, name, ext))
        return photos
    finally:
        if useFlash:
            CameraFlash(False)


def CameraFlash(on):
    if isunicornhatattached:
        myunicornhat.CameraFlash(on)
    if ispiglowattached:
        MyPiglow.CameraFlash(on)
    if isbrightpiattached and brightpi:
        brightpi.CameraFlash(on)


def Lights():
    if isunicornhatattached:
        myunicornhat.Lights()
    if ispiglowattached:
        MyPiglow.Lights()


def OnLightsScheduledTask():
    if isunicornhatattached:
        myunicornhat.OnLightsScheduledTask()
    if ispiglowattached:
        MyPiglow.OnLightsScheduledTask()


def Fade():
    if isunicornhatattached:
        myunicornhat.Fade()
    if ispiglowattached:
        MyPiglow.Fade()


def inbox_item_received(inbox_item):
    if isunicornhatattached:
        myunicornhat.inbox_item_received(inbox_item)
    if ispiglowattached:
        MyPiglow.Oninbox_itemRecieved(inbox_item)


def Stop():
    if iswebcamattached and webcam:
        webcam.Close()
    if ispicamattached and picam:
        picam.Close()
    if isunicornhatattached:
        myunicornhat.Close()
    if ispiglowattached:
        MyPiglow.Close()
    if isbrightpiattached and brightpi:
        brightpi.Close()
