from ScheduledTask import ScheduledTask
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter
import urllib
import MyQueues


UK_WOEID = 23424975
US_WOEID = 23424977
woeids = cycle([UK_WOEID, US_WOEID])

class TrendsScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self._trendsList = []

    def GetTrigger(args):
        return IntervalTrigger(minutes=29)

    def onRun(args):
        with MyTwitter() as twitter:
            if not args._trendsList:
                woeid = next(woeids)
                trends = twitter.get_place_trends(id = woeid)[0].get('trends',[])   
                args._trendsList.extend(trends)

            trend = args._trendsList.pop()
            trendtweets = twitter.search(q = urllib.quote_plus(trend["name"]), result_type = "popular")
            for trendtweet in trendtweets["statuses"]:
                trendtweet['tweetsource'] = "trend:" + trend["name"]
                MyQueues.inbox.put(trendtweet)

    