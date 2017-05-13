import logging
import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.data_access.dal import housekeeping
from twitterpibot.schedule.ScheduledTask import ScheduledTask

__author__ = 'Andrew'

logger = logging.getLogger(__name__)


class HousekeepingScheduledTask(ScheduledTask):
    def __init__(self, identity):
        ScheduledTask.__init__(self, identity)

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(24, 48), minutes=random.randint(0, 59))

    def on_run(self):
        logger.info("Housekeeping...")
        housekeeping()
        logger.info("Housekeeping done.")


if __name__ == '__main__':
    import identities_pis

    logging.basicConfig(level=logging.INFO)
    identity = identities_pis.AndrewTathamPiIdentity()
    task = HousekeepingScheduledTask(identity)
    task.on_run()
