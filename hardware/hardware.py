import subprocess
import platform

iswindows = False
isRaspbian = False

isAndrewDesktop = False
isAndrewLaptop = False
isRaspberryPi = False
isRaspberryPi2 = False

ispiglowattached = False
ispicamattached = False
iswebcamattached = False
isbrightpiattached = False
isunicornhatattached = False

picam = None
webcam = None
brightpi = None
unicornhat = None

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
        iswebcamattached = True
    elif isAndrewLaptop:
        iswebcamattached = True

elif isRaspbian:

    test = subprocess.Popen(["sudo","i2cdetect","-y","1"], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    print(str(output))

    if isRaspberryPi:
        ispicamattached = True
        ispiglowattached = True # bool(" 54 " in output)
        isbrightpiattached = bool(" 70 " in output)
    elif isRaspberryPi2:
        iswebcamattached = True
        isunicornhatattached = True
           
        
if iswebcamattached:
    import MyWebcam
    webcam = MyWebcam.Webcam()
if ispicamattached:
    import MyPicam
    picam = MyPicam.MyPicam()
if isunicornhatattached:
    import myunicornhat
    unicornhat = myunicornhat.MyUnicornHat()
if ispiglowattached:
    import MyPiglow
if isbrightpiattached:
    import MyBrightPi
    brightpi = MyBrightPi.BrightPI()


def TakePhotoToDisk(dir, name, ext):
    try:
        CameraFlash(True)
        photos = []
        if iswebcamattached and webcam:
            photos.append(webcam.TakePhotoToDisk(dir, name, ext))
        if ispicamattached and picam:
            photos.append(picam.TakePhotoToDisk(dir, name, ext))
        return photos
    finally:
        CameraFlash(False)


def CameraFlash(on):
    if isunicornhatattached and unicornhat:
        unicornhat.CameraFlash(on)
    if ispiglowattached:
        MyPiglow.CameraFlash(on)
    if isbrightpiattached and brightpi:
        brightpi.CameraFlash(on)

def Fade():
    if isunicornhatattached and unicornhat:
        unicornhat.Fade()
    if ispiglowattached:
        MyPiglow.Fade()

def OnInboxItemRecieved(inboxItem):
    if isunicornhatattached and unicornhat:
        unicornhat.OnInboxItemRecieved(inboxItem)
    if ispiglowattached:
        MyPiglow.OnInboxItemRecieved(inboxItem)

def Stop():
    if iswebcamattached and webcam:
        webcam.Close()
    if ispicamattached and picam:
        picam.Close()
    if isunicornhatattached and unicornhat:
        unicornhat.Close()
    if ispiglowattached:
        MyPiglow.Close()
    if isbrightpiattached and brightpi:
        brightpi.Close()