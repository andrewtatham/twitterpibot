from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.twitter import TrendingTopics
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.twitter import TwitterHelper
import twitterpibot.MyQueues as MyQueues


class TrendsScheduledTask(ScheduledTask):
    def __init__(self):
        self._trendsList = []
        super(TrendsScheduledTask, self).__init__()

    def get_trigger(self):
        return IntervalTrigger(minutes=45)

    def on_run(self):
        if not self._trendsList:
            self._trendsList = TrendingTopics.get()

        if self._trendsList:
            trend = self._trendsList.pop()
            trendtweets = TwitterHelper.search(trend.text)
            for trendtweet in trendtweets:
                trendtweet['tweet_source'] = "trend:" + trend.text
                MyQueues.inbox.put(trendtweet)
