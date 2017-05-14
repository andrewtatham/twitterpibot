import logging

from twitterpibot.hardware import myperipherals
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)


class LightsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=3)

    def on_run(self):
        logger.info("LightsScheduledTask on_run")
        myperipherals.on_lights_scheduled_task()
