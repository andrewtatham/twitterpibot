from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import Send


class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=7)

    def onRun(self):
        Send(OutgoingTweet(text="@BBCWeatherBot Leeds Today"))
