from ScheduledTask import ScheduledTask
from colorama import Fore, Style
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter
from Queue import Queue
from apscheduler.triggers.cron import CronTrigger
import urllib
from collections import Counter
from OutgoingTweet import OutgoingTweet
import random


worldwide_WOEID = 1
UK_WOEID = 23424975
US_WOEID = 23424977
leeds_WOEID = 26042

woeids = cycle([UK_WOEID, US_WOEID])

trendColours = cycle([Fore.MAGENTA, Fore.WHITE])

class TrendsScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self._trendsList = Queue()

    def GetTrigger(args):
        return IntervalTrigger(minutes=29)

    def onRun(args):
        with MyTwitter() as twitter:


            if args._trendsList.empty():
                woeid = woeids.next()
                trends = twitter.get_place_trends(id = woeid)[0].get('trends',[])   
                for trend in trends:
                    colour = trendColours.next()
                    print(colour + "Trends: [" + trend['name'] + "]")
                args._trendsList.put(trend)

            try:
                trend = args._trendsList.get()
                trendtweets = twitter.search(q = urllib.quote_plus(trend["name"]), result_type = "popular")

                trendText = ""
                for trendtweet in trendtweets["statuses"]:
                    colour = trendColours.next()
                    trendText += " " + trendtweet["text"].replace("\n", "   ")
                    print(colour + "Trend: [" + trend["name"] + "] - " \
                        + trendtweet["user"]["name"] + " [@" + trendtweet["user"]["screen_name"] + "] - "\
                        + trendtweet["text"].replace("\n", "   "))

                trendtweet = random.choice(trendtweets["statuses"])
                twitter.retweet(id = trendtweet["id_str"])

                # TODO reply?
            finally:
                args._trendsList.task_done()

    