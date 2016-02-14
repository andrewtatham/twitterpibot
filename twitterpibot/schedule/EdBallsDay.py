from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

import datetime



class EdBallsDay(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(month=4, day=28, hour=16, minute=20)

    def on_run(self):
        year = str(datetime.date.today().year)
        text = "@edballs ED BALLS #EdBallsDay #EdBallsDay" + year
        tweet = OutgoingTweet(text=text)
        self.identity.twitter.send(tweet)
