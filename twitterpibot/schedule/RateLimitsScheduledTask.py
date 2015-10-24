from apscheduler.triggers.interval import IntervalTrigger

from ScheduledTask import ScheduledTask
from twitterpibot.twitter.MyTwitter import MyTwitter

filename = "RATE_LIMITS.pkl"


class RateLimitsScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(minutes=20)

    def onRun(self):
        # https://dev.twitter.com/rest/public/rate-limiting
        # https://dev.twitter.com/rest/public/rate-limits
        # https://dev.twitter.com/rest/reference/get/application/rate_limit_status

        with MyTwitter() as twitter:
            rates = twitter.get_application_rate_limit_status()
            ratelimits.UpdateRateLimits(rates)
