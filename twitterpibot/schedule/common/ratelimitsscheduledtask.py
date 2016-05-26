from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask


class RateLimitsScheduledTask(ScheduledTask):

    def get_trigger(self):
        return IntervalTrigger(minutes=5)

    def on_run(self):
        self.identity.twitter.update_rate_limits()
