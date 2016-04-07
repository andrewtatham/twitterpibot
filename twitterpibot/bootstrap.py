import logging

import colorama

from twitterpibot import loggingconfig
from twitterpibot import hardware, tasks, schedule
from twitterpibot import webserver

if not hardware.is_andrew_desktop:
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

    logger.info("Setting tasks")
    tasks.set_tasks(all_identities)
    logger.info("Setting schedule")
    schedule.set_scheduled_jobs(all_identities)
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
    hardware.stop()

    logger.info(obviousness + " Stopped " + obviousness)
