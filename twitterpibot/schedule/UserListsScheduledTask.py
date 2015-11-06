from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.twitter import Lists


class UserListsScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(minute="5/15")

    def onRun(self):
        Lists.update_lists()
