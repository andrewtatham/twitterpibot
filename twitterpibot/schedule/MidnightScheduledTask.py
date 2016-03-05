from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage


class MidnightScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=0)

    def on_run(self):
        stats = self.identity.statistics.get_statistics()
        self.identity.statistics.reset()
        self.identity.twitter.send(OutgoingDirectMessage(text=stats))
