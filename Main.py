import sys
import logging

import colorama

import twitterpibot.hardware.hardware as hardware
import twitterpibot.Identity as Identity
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule
import twitterpibot.MyUI as MyUI
import twitterpibot.MyLogging as MyLogging

MyLogging.init()
logger = logging.getLogger(__name__)

Identity.init()

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

Tasks.start()
MySchedule.start()

MyUI.start()

MySchedule.stop()
Tasks.stop()
hardware.stop()
print("Done")
sys.exit(0)
