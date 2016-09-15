import os
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
    import wmi

    if is_andrew_desktop:
        is_webcam_attached = False
    elif is_andrew_laptop:
        is_webcam_attached = True

elif is_mac_osx:
    if is_andrew_macbook:
        is_webcam_attached = False
        is_blinksticknano_attached = False
        is_unicornhat_attached = True


elif is_linux:

    test = subprocess.Popen(["sudo", "i2cdetect", "-y", "1"], stdout=subprocess.PIPE)
    output = str(test.communicate()[0])
    logger.debug(output)

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


def get_remaining_disk_space():
    free_space_mb = None
    if is_windows:
        c = wmi.WMI()
        # TODO CHECK/FIX disk space on windows
        for d in c.Win32_LogicalDisk():
            print(d.Caption, d.FreeSpace, d.Size, d.DriveType)
            free_space_mb = d.FreeSpace / 1024 / 1024

    else:
        path = "/"

        st = os.statvfs(path)
        logger.debug(st)
        free_space_mb = st.f_bavail * st.f_frsize / 1024 / 1024 

    return free_space_mb


if __name__ == '__main__':
    print(get_remaining_disk_space())
