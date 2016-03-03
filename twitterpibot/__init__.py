import logging

import colorama
import twitterpibot.hardware
import twitterpibot.identities
import twitterpibot.logic
import twitterpibot.processing
import twitterpibot.responses
import twitterpibot.schedule
import twitterpibot.tasks
import twitterpibot.MyLogging
import twitterpibot.controller

logger = logging.getLogger(__name__)

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)


def start():
    logger.info("Setting tasks")
    twitterpibot.tasks.set_tasks(twitterpibot.identities.get_all_tasks())
    logger.info("Setting schedule")
    twitterpibot.schedule.set_scheduled_jobs(twitterpibot.identities.get_all_scheduled_jobs())
    logger.info("Starting tasks")
    twitterpibot.tasks.start()
    logger.info("Starting schedule")
    twitterpibot.schedule.start()
    logger.info("Started")


def stop():
    logger.info("Stopping schedule")
    twitterpibot.schedule.stop()
    logger.info("Stopping tasks")
    twitterpibot.tasks.stop()
    logger.info("Stopping hardware")
    twitterpibot.hardware.stop()
    logger.info("Stopped")
