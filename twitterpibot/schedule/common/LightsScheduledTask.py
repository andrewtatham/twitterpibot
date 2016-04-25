from twitterpibot.hardware import myperipherals
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger


class LightsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=3)

    def on_run(self):
        myperipherals.on_lights_scheduled_task()
