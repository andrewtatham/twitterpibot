import subprocess
import platform
import logging

logger = logging.getLogger(__name__)

is_piglow_attached = False
is_picam_attached = False
is_webcam_attached = False
is_brightpi_attached = False
is_unicornhat_attached = False
is_blinksticknano_attached = False

picam = None
webcam = None
brightpi = None

_platform = platform.platform()
logger.info("platform: %s", _platform)
is_windows = _platform.startswith('Windows')
is_mac_osx = _platform.startswith('Darwin')
is_linux = _platform.startswith('Linux')

_node = platform.node()
logger.info("node: " + _node)
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
        is_blinksticknano_attached = False


elif is_linux:

    test = subprocess.Popen(["sudo", "i2cdetect", "-y", "1"], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    logger.debug(str(output))

    if is_raspberry_pi:
        is_webcam_attached = False
        is_picam_attached = True
        is_piglow_attached = False  # bool(" 54 " in output)
        is_brightpi_attached = bool(" 70 " in output)
    elif is_raspberry_pi_2:
        is_webcam_attached = False
        is_unicornhat_attached = False

logger.info("is_webcam_attached: %s", is_webcam_attached)
logger.info("is_picam_attached: %s", is_picam_attached)
logger.info("is_unicornhat_attached: %s", is_unicornhat_attached)
logger.info("is_piglow_attached: %s", is_piglow_attached)
logger.info("is_brightpi_attached: %s", is_brightpi_attached)

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
    # noinspection PyUnresolvedReferences
    brightpi = MyBrightPi.BrightPI()
if is_blinksticknano_attached:
    import twitterpibot.hardware.MyBlinkstickNano as MyBlinkstickNano


def take_photo(dir, name, ext, use_flash=False):
    try:
        if use_flash:
            camera_flash(True)
        photos = []
        if is_webcam_attached and webcam:
            photos.append(webcam.TakePhotoToDisk(dir, name, ext))
        if is_picam_attached and picam:
            photos.append(picam.TakePhotoToDisk(dir, name, ext))
        return photos
    finally:
        if use_flash:
            camera_flash(False)


def camera_flash(on):
    if is_unicornhat_attached:
        myunicornhat.camera_flash(on)
    if is_piglow_attached:
        MyPiglow.camera_flash(on)
    if is_brightpi_attached and brightpi:
        brightpi.camera_flash(on)
    if is_blinksticknano_attached:
        MyBlinkstickNano.camera_flash(on)


def on_lights_task():
    if is_unicornhat_attached:
        myunicornhat.lights()
    if is_piglow_attached:
        MyPiglow.lights()
    if is_blinksticknano_attached:
        MyBlinkstickNano.lights()


def on_lights_scheduled_task():
    if is_unicornhat_attached:
        myunicornhat.on_lights_scheduled_task()
    if is_piglow_attached:
        MyPiglow.on_lights_scheduled_task()
    if is_blinksticknano_attached:
        MyBlinkstickNano.on_lights_scheduled_task()


def on_fade_task():
    if is_unicornhat_attached:
        myunicornhat.fade()
    if is_piglow_attached:
        MyPiglow.fade()
    if is_blinksticknano_attached:
        MyBlinkstickNano.fade()


def on_inbox_item_received(inbox_item):
    if is_unicornhat_attached:
        myunicornhat.inbox_item_received(inbox_item)
    if is_piglow_attached:
        MyPiglow.inbox_item_received(inbox_item)
    if is_blinksticknano_attached:
        MyBlinkstickNano.inbox_item_received(inbox_item)


def stop():
    logger.info("Stopping")
    if is_webcam_attached and webcam:
        webcam.close()
    if is_picam_attached and picam:
        picam.close()
    if is_unicornhat_attached:
        myunicornhat.close()
    if is_piglow_attached:
        MyPiglow.close()
    if is_brightpi_attached and brightpi:
        brightpi.close()
    if is_blinksticknano_attached:
        MyBlinkstickNano.close()
    logger.info("Stopped")
