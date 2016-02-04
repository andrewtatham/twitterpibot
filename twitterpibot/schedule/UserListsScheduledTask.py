from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.twitter import Lists


class UserListsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute="5/15")

    def on_run(self):
        Lists.update_lists()
