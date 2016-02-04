from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.twitter.TwitterHelper import send


class BlankTweetScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=35)

    def on_run(self):
        send(OutgoingTweet(text="This tweet intentionally left blank"))
