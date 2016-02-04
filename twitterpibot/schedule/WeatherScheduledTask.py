from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


class WeatherScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=7)

    def on_run(self):
        send(OutgoingTweet(text="@BBCWeatherBot Leeds Today"))
