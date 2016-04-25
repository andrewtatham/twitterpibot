import logging

import colorama

from twitterpibot import tasks, schedule, webserver, loggingconfig
from twitterpibot.hardware import myhardware, myperipherals
from twitterpibot.schedule import GlobalMonitorScheduledTask
from twitterpibot.tasks.FadeTask import FadeTask
from twitterpibot.tasks.LightsTask import LightsTask

if not myhardware.is_andrew_desktop:
    colorama.init(autoreset=True)

# import textblob.download_corpora
#
# textblob.download_corpora.download_lite()
loggingconfig.init()

__author__ = 'andrewtatham'

logger = logging.getLogger(__name__)
all_identities = []


def run(identities):
    global all_identities
    all_identities = identities
    obviousness = "=" * 5
    logger.info(obviousness + " Starting " + obviousness)

    set_tasks(identities)

    set_scheduled_jobs(all_identities)

    logger.info("Starting tasks")
    tasks.start()
    logger.info("Starting schedule")
    schedule.start()

    logger.info(obviousness + " Starting UI " + obviousness)
    webserver.app.run(debug=False, host='0.0.0.0')
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
        GlobalMonitorScheduledTask(None)
    ]
    for identity in identities:
        _scheduled_jobs.extend(identity.get_scheduled_jobs())
    schedule.set_scheduled_jobs(_scheduled_jobs)


def set_tasks(identities):
    logger.info("Setting tasks")
    _tasks = []
    if myhardware.is_piglow_attached \
            or myhardware.is_unicornhat_attached \
            or myhardware.is_blinksticknano_attached:
        _tasks.extend([
            LightsTask(),
            FadeTask()
        ])
    for identity in identities:
        _tasks.extend(identity.get_tasks())
    tasks.set_tasks(_tasks)
