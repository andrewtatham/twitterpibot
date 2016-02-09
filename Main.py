import sys
import logging

import colorama

import twitterpibot.Identity
import twitterpibot.MyLogging as MyLogging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule
import twitterpibot.MyUI as MyUI

MyLogging.init()
logger = logging.getLogger(__name__)

twitterpibot.Identity.init()

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

Tasks.start()
MySchedule.start()

MyUI.start()

MySchedule.stop()
Tasks.stop()
hardware.stop()
logger.info("Done")
sys.exit(0)
