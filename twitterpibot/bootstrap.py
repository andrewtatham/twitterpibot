import logging

import colorama

from twitterpibot import tasks, schedule, webserver, loggingconfig, controller
from twitterpibot.hardware import myhardware, myperipherals
from twitterpibot.schedule import GlobalMonitorScheduledTask
from twitterpibot.schedule.common.LightsScheduledTask import LightsScheduledTask
from twitterpibot.schedule.common.database_scheduled_tasks import HousekeepingScheduledTask
from twitterpibot.tasks.LightsTask import LightsTask

if not myhardware.is_andrew_desktop:
    colorama.init(autoreset=True)

# import textblob.download_corpora
#
# textblob.download_corpora.download_lite()


__author__ = 'andrewtatham'

logger = logging.getLogger(__name__)


def run(identities):
    obviousness = "=" * 5
    logger.info(obviousness + " Starting " + obviousness)

    set_tasks(identities)

    set_scheduled_jobs(identities)

    logger.info("Starting tasks")
    tasks.start()
    logger.info("Starting schedule")
    schedule.start()
    loggingconfig.mute_scheduler()

    logger.info(obviousness + " Starting UI " + obviousness)
    controller.set_identities(identities)
    webserver.run()
    logger.info(obviousness + " Stopped UI " + obviousness)

    logger.info("Stopping schedule")
    schedule.stop()
    logger.info("Stopping tasks")
    tasks.stop()
    logger.info("Stopping hardware")
    myperipherals.stop()

    logger.info(obviousness + " Stopped " + obviousness)


def set_scheduled_jobs(identities):
    logger.info("Setting schedule")
    _scheduled_jobs = [
        HousekeepingScheduledTask(None)
    ]
    if not myhardware.is_windows:
        _scheduled_jobs.extend([
            GlobalMonitorScheduledTask(None)
        ])

    if myhardware.is_lights_attached:
        _scheduled_jobs.extend([
            LightsScheduledTask(None)
        ])
    for identity in identities:
        _scheduled_jobs.extend(identity.get_scheduled_jobs())
    schedule.set_scheduled_jobs(_scheduled_jobs)


def set_tasks(identities):
    logger.info("Setting tasks")
    _tasks = []
    if myhardware.is_lights_attached:
        _tasks.extend([
            LightsTask()
        ])

    for identity in identities:
        _tasks.extend(identity.get_tasks())
    tasks.set_tasks(_tasks)
