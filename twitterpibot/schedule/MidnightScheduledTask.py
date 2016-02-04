from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.Statistics import get_statistics, reset
from twitterpibot.twitter.TwitterHelper import send


class MidnightScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=0)

    def on_run(self):
        stats = get_statistics()
        send(OutgoingDirectMessage(text=stats))
        reset()
