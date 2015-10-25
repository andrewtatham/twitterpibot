import subprocess
import platform

is_piglow_attached = False
is_picam_attached = False
is_webcam_attached = False
is_brightpi_attached = False
is_unicornhat_attached = False

picam = None
webcam = None
brightpi = None

_platform = platform.platform()
print("platform: " + _platform)
is_windows = _platform.startswith('Windows')
is_mac_osx = _platform.startswith('Darwin')
is_linux = _platform.startswith('Linux')

_node = platform.node()
print("node: " + _node)
is_andrew_desktop = _node == "ANDREWDESKTOP"
is_andrew_laptop = _node == "ANDREWLAPTOP"
is_raspberry_pi = _node == "raspberrypi"
is_raspberry_pi_2 = _node == "raspberrypi2"
is_andrew_macbook = _node == "Andrews-MacBook-Pro.local"

if is_windows:

    if is_andrew_desktop:
        is_webcam_attached = False
    elif is_andrew_laptop:
        is_webcam_attached = True

elif is_mac_osx:
    if is_andrew_macbook:
        is_webcam_attached = False

elif is_linux:

    test = subprocess.Popen(["sudo", "i2cdetect", "-y", "1"], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    print(str(output))

    if is_raspberry_pi:
        is_webcam_attached = True
        is_picam_attached = False
        is_piglow_attached = True  # bool(" 54 " in output)
        is_brightpi_attached = bool(" 70 " in output)
    elif is_raspberry_pi_2:
        is_webcam_attached = False
        is_unicornhat_attached = True

if is_webcam_attached:
    import twitterpibot.hardware.MyWebcam as MyWebcam
    webcam = MyWebcam.Webcam()
if is_picam_attached:
    import twitterpibot.hardware.MyPicam as MyPicam
    picam = MyPicam.MyPicam()
if is_unicornhat_attached:
    import twitterpibot.hardware.myunicornhat as myunicornhat
if is_piglow_attached:
    import twitterpibot.hardware.MyPiglow as MyPiglow
if is_brightpi_attached:
    import twitterpibot.hardware.MyBrightPi as MyBrightPi

    brightpi = MyBrightPi.BrightPI()


def TakePhotoToDisk(dir, name, ext, useFlash=False):
    try:
        if useFlash:
            CameraFlash(True)
        photos = []
        if is_webcam_attached and webcam:
            photos.append(webcam.TakePhotoToDisk(dir, name, ext))
        if is_picam_attached and picam:
            photos.append(picam.TakePhotoToDisk(dir, name, ext))
        return photos
    finally:
        if useFlash:
            CameraFlash(False)


def CameraFlash(on):
    if is_unicornhat_attached:
        myunicornhat.CameraFlash(on)
    if is_piglow_attached:
        MyPiglow.CameraFlash(on)
    if is_brightpi_attached and brightpi:
        brightpi.CameraFlash(on)


def Lights():
    if is_unicornhat_attached:
        myunicornhat.Lights()
    if is_piglow_attached:
        MyPiglow.Lights()


def OnLightsScheduledTask():
    if is_unicornhat_attached:
        myunicornhat.OnLightsScheduledTask()
    if is_piglow_attached:
        MyPiglow.OnLightsScheduledTask()


def Fade():
    if is_unicornhat_attached:
        myunicornhat.Fade()
    if is_piglow_attached:
        MyPiglow.Fade()


def inbox_item_received(inbox_item):
    if is_unicornhat_attached:
        myunicornhat.inbox_item_received(inbox_item)
    if is_piglow_attached:
        MyPiglow.Oninbox_itemRecieved(inbox_item)


def Stop():
    if is_webcam_attached and webcam:
        webcam.Close()
    if is_picam_attached and picam:
        picam.Close()
    if is_unicornhat_attached:
        myunicornhat.Close()
    if is_piglow_attached:
        MyPiglow.Close()
    if is_brightpi_attached and brightpi:
        brightpi.Close()
