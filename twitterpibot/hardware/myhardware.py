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
        is_unicornhat_attached = True

logger.info("is_webcam_attached: %s", is_webcam_attached)
logger.info("is_picam_attached: %s", is_picam_attached)
logger.info("is_unicornhat_attached: %s", is_unicornhat_attached)
logger.info("is_piglow_attached: %s", is_piglow_attached)
logger.info("is_brightpi_attached: %s", is_brightpi_attached)

