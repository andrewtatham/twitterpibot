import pyjokes
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.twitter.TwitterHelper import Send


class JokesScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*/2")

    def onRun(self):
        text = pyjokes.get_joke()
        Send(OutgoingTweet(text=text))
