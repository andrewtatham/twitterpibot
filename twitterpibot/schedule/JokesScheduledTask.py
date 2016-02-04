import pyjokes
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.twitter.TwitterHelper import send


class JokesScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="*/2")

    def on_run(self):
        text = pyjokes.get_joke()
        send(OutgoingTweet(text=text))
