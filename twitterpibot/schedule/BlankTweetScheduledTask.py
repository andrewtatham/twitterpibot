from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class BlankTweetScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=17, minutes=2)

    def on_run(self):
        self.identity.twitter.send(OutgoingTweet(text="This tweet intentionally left blank"))
