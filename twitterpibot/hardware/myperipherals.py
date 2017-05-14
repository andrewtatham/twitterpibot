import logging

from twitterpibot.hardware import myhardware

logger = logging.getLogger(__name__)

if myhardware.is_webcam_attached:
    from twitterpibot.hardware import MyWebcam as MyWebcam
if myhardware.is_picam_attached:
    from twitterpibot.hardware import MyPicam as MyPicam
if myhardware.is_unicornhat_attached:
    from twitterpibot.hardware.unicorn import myunicornhat as myunicornhat
if myhardware.is_piglow_attached:
    from twitterpibot.hardware import MyPiglow as MyPiglow
brightpi = None
if myhardware.is_brightpi_attached:
    from twitterpibot.hardware import MyBrightPi as MyBrightPi

    # noinspection PyUnresolvedReferences
    brightpi = MyBrightPi.BrightPI()
if myhardware.is_blinksticknano_attached:
    from twitterpibot.hardware import MyBlinkstickNano as MyBlinkstickNano
if myhardware.is_scroll_hat_attached:
    from twitterpibot.hardware import myscrollhat


def take_photo(folder, name, ext, use_flash=False):
    try:
        if use_flash:
            camera_flash(True)
        photos = []
        if myhardware.is_webcam_attached:
            photos.append(MyWebcam.take_photo(folder, name, ext))
        if myhardware.is_picam_attached:
            photos.append(MyPicam.take_photo(folder, name, ext))
        return photos
    finally:
        if use_flash:
            camera_flash(False)


def camera_flash(on):
    if myhardware.is_unicornhat_attached:
        myunicornhat.camera_flash(on)
    if myhardware.is_piglow_attached:
        MyPiglow.camera_flash(on)
    if myhardware.is_brightpi_attached and brightpi:
        brightpi.camera_flash(on)
    if myhardware.is_blinksticknano_attached:
        MyBlinkstickNano.camera_flash(on)


def on_lights_task():
    if myhardware.is_unicornhat_attached:
        myunicornhat.lights()
    if myhardware.is_piglow_attached:
        MyPiglow.lights()
    if myhardware.is_blinksticknano_attached:
        MyBlinkstickNano.lights()
    if myhardware.is_scroll_hat_attached:
        myscrollhat.lights()


def on_lights_scheduled_task():
    if myhardware.is_unicornhat_attached:
        myunicornhat.on_lights_scheduled_task()
    if myhardware.is_piglow_attached:
        MyPiglow.on_lights_scheduled_task()
    if myhardware.is_blinksticknano_attached:
        MyBlinkstickNano.on_lights_scheduled_task()
    if myhardware.is_scroll_hat_attached:
        myscrollhat.on_lights_scheduled_task()

def on_fade_task():
    if myhardware.is_unicornhat_attached:
        myunicornhat.fade()
    if myhardware.is_piglow_attached:
        MyPiglow.fade()
    if myhardware.is_blinksticknano_attached:
        MyBlinkstickNano.fade()


def on_inbox_item_received(inbox_item):
    if myhardware.is_unicornhat_attached:
        myunicornhat.inbox_item_received(inbox_item)
    if myhardware.is_piglow_attached:
        MyPiglow.inbox_item_received(inbox_item)
    if myhardware.is_blinksticknano_attached:
        MyBlinkstickNano.inbox_item_received(inbox_item)
    if myhardware.is_scroll_hat_attached:
        myscrollhat.inbox_item_received(inbox_item)


def stop():
    logger.info("Stopping")
    if myhardware.is_unicornhat_attached:
        myunicornhat.close()
    if myhardware.is_picam_attached:
        MyPicam.close()
    if myhardware.is_webcam_attached:
        MyWebcam.close()
    if myhardware.is_piglow_attached:
        MyPiglow.close()
    if myhardware.is_brightpi_attached and brightpi:
        brightpi.close()
    if myhardware.is_blinksticknano_attached:
        MyBlinkstickNano.close()
    if myhardware.is_scroll_hat_attached:
        myscrollhat.close()
    logger.info("Stopped")
