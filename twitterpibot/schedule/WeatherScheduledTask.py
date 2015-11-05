from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=7)

    def onRun(self):
        send(OutgoingTweet(text="@BBCWeatherBot Leeds Today"))
