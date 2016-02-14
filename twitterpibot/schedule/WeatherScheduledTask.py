from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet


class WeatherScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=7)

    def on_run(self):
        self.identity.twitter.send(OutgoingTweet(text="@BBCWeatherBot Leeds Today"))
