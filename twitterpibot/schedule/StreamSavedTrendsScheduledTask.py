from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.twitter.MyTwitter import MyTwitter
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.tasks import Tasks
from twitterpibot.twitter import TwitterHelper

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

UK_WOEID = 23424975
US_WOEID = 23424977
woeids = [UK_WOEID, US_WOEID]

class StreamSavedTrendsScheduledTask(ScheduledTask):
    


    def GetTrigger(self):
        return IntervalTrigger(minutes=45)


    def onRun(self):
        with MyTwitter() as twitter:
            saved_list = twitter.get_saved_searches()
            trends_list = []
            for woeid in woeids:
                trends = twitter.get_place_trends(id=woeid)[0].get('trends', [])
                trends_list.extend(trends)

        stream_list = Tasks.get()
                
        # Check for new trends that are also saved searches
        for trend in trends_list:
            if trend in saved_list and trend not in stream_list:
                # Create stream
                Tasks.add(StreamTweetsTask(TwitterHelper.GetStreamer(), topic=trend))

        # Check for streams that are no longer trending or not saved
        for trend_stream in stream_list:
            if trend_stream not in saved_list or trend_stream not in trends_list:
                # stop stream
                Tasks.remove(trend_stream)


