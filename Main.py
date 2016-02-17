import sys
import logging
import webbrowser

import colorama

import twitterpibot.MyLogging as MyLogging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.identities
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule

# import twitterpibot.MyUI as MyUI
import twitterpibot.ui.MyWebUI

MyLogging.init()
logger = logging.getLogger(__name__)

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)


tasks = twitterpibot.identities.get_all_tasks()
Tasks.set_tasks(tasks)

jobs = twitterpibot.identities.get_all_scheduled_jobs()
MySchedule.set_scheduled_jobs(jobs)

Tasks.start()
MySchedule.start()

# MyUI.start()
twitterpibot.ui.MyWebUI.start()


MySchedule.stop()
Tasks.stop()
hardware.stop()
logger.info("Done")
sys.exit(0)
