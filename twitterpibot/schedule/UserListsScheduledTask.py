from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask


class UserListsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute="5/15")

    def on_run(self):
        self.identity.lists.update_lists()
