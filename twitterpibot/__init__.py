import logging

import colorama
import twitterpibot.responses
import twitterpibot.schedule
import twitterpibot.tasks
import twitterpibot.Controller as c
import twitterpibot.MyLogging as mylogging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.identities as identities
import twitterpibot.schedule.MySchedule as myschedule
import twitterpibot.tasks.tasks as mytasks


mylogging.init()
logger = logging.getLogger(__name__)

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

logger.info("Starting")
mytasks.set_tasks(identities.get_all_tasks())
myschedule.set_scheduled_jobs(identities.get_all_scheduled_jobs())
mytasks.start()
myschedule.start()
