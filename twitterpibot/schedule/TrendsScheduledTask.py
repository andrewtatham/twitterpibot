from ScheduledTask import ScheduledTask
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.twitter.MyTwitter import MyTwitter

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
import twitterpibot.MyQueues as MyQueues

UK_WOEID = 23424975
US_WOEID = 23424977
woeids = cycle([UK_WOEID, US_WOEID])


class TrendsScheduledTask(ScheduledTask):
    def __init__(self):
        self._trendsList = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=29)

    def onRun(self):
        with MyTwitter() as twitter:
            if not self._trendsList:
                woeid = next(woeids)
                trends = twitter.get_place_trends(id=woeid)[0].get('trends', [])
                self._trendsList.extend(trends)

            if self._trendsList:
                trend = self._trendsList.pop()
                trendtweets = twitter.search(q=quote_plus(trend["name"]), result_type="popular")
                for trendtweet in trendtweets["statuses"]:
                    trendtweet['tweetsource'] = "trend:" + trend["name"]
                    MyQueues.inbox.put(trendtweet)
