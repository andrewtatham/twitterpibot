from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.Statistics import get_statistics, reset



class MidnightScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=0)

    def on_run(self):
        stats = get_statistics()
        self.identity.twitter.send(OutgoingDirectMessage(text=stats))
        reset()
