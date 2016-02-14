import sys
import logging

import colorama

import twitterpibot.MyLogging as MyLogging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule
import twitterpibot.MyUI as MyUI

MyLogging.init()
logger = logging.getLogger(__name__)

import twitterpibot.identitymanager as identitymanager

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

identitymanager.init()
Tasks.set_tasks(identitymanager.get_tasks())
MySchedule.set_scheduled_jobs(identitymanager.get_scheduled_jobs())

Tasks.start()
MySchedule.start()

MyUI.start()

MySchedule.stop()
Tasks.stop()
hardware.stop()
logger.info("Done")
sys.exit(0)
