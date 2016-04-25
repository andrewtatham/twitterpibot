from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import twitterpibot.hardware.myhardware


class LightsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=3)

    def on_run(self):
        twitterpibot.hardware.myhardware.on_lights_scheduled_task()
