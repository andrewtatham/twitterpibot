import logging

import twitterpibot.Identity
import twitterpibot.hardware.hardware as hardware

logger = logging.getLogger(__name__)

identities = []


def init():
    if hardware.is_raspberry_pi:
        identities.append(twitterpibot.Identity.andrewtathampi())
    elif hardware.is_raspberry_pi_2:
        identities.extend([
            twitterpibot.Identity.andrewtatham(),
            twitterpibot.Identity.andrewtathampi2(),
            twitterpibot.Identity.numberwang_host()])
    else:
        identities.extend([
            twitterpibot.Identity.andrewtathampi(),
            twitterpibot.Identity.andrewtathampi2(),
            twitterpibot.Identity.andrewtatham(),
            twitterpibot.Identity.numberwang_host()
        ])

    for identity in identities:
        identity.init()
        logger.info("Identity: " + identity.screen_name)


def get_tasks():
    tasks = []
    for identity in identities:
        tasks.extend(identity.get_tasks())
    return tasks


def get_responses():
    responses = []
    for identity in identities:
        responses.append(identity.get_responses())
    return responses


def get_scheduled_jobs():
    scheduled_jobs = []
    for identity in identities:
        scheduled_jobs.extend(identity.get_scheduled_jobs())
    return scheduled_jobs
