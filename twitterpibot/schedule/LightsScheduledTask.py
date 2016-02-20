from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import twitterpibot.hardware


class LightsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=3)

    def on_run(self):
        twitterpibot.hardware.on_lights_scheduled_task()
