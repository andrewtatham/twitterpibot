from ScheduledTask import ScheduledTask
import pprint
import pickle
import os
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter



filename = "RATE_LIMITS.pkl"

class RateLimitsScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return IntervalTrigger(minutes=20)


    def onRun(args):
        # https://dev.twitter.com/rest/public/rate-limiting
        # https://dev.twitter.com/rest/public/rate-limits
        # https://dev.twitter.com/rest/reference/get/application/rate_limit_status

        with MyTwitter() as twitter:
            rates = twitter.get_application_rate_limit_status()
            ratelimits.UpdateRateLimits(rates)


    def onInit(args):

        if os.path.isfile(filename):
            ratelimits = pickle.load(open(filename, "rb"))
        else:
            args.onRun()

    def onStop(args):
        if ratelimits:
            pickle.dump(ratelimits, open(filename, "wb"))

        
