import datetime

from apscheduler.triggers.interval import IntervalTrigger

from outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.tasks import Tasks
from twitterpibot.twitter import TwitterHelper, SavedSearches, TrendingTopics
from twitterpibot.processing import OneDirection
from twitterpibot.twitter.TwitterHelper import Send


class StreamTrendsScheduledTask(ScheduledTask):
    


    def GetTrigger(self):
        return IntervalTrigger(minutes=5)


    def onRun(self):
        saved_list = SavedSearches.get_saved_searches()
        trends_list = TrendingTopics.get()
        stream_list = Tasks.get()
                
        # Check for new trends that are also saved searches
        for trend in trends_list:

            is_one_direction = OneDirection.is_one_direction(trend)
            is_saved = trend in saved_list
            is_streaming = trend in stream_list

            if (is_saved or is_one_direction) and not is_streaming:
                # Create stream
                Tasks.add(StreamTweetsTask(TwitterHelper.GetStreamer(), topic=trend))
                Send(OutgoingDirectMessage(text = "Starting stream " + trend + " " + str(datetime.datetime.now())))

        # Check for streams that are no longer trending or not saved
        for trend in stream_list:

            is_one_direction = OneDirection.is_one_direction(trend)
            is_saved = trend in saved_list
            is_trending = trend in trends_list

            if not is_trending or not is_saved and not is_one_direction:
                # stop stream
                Send(OutgoingDirectMessage(text = "Stopping stream " + trend + " " + str(datetime.datetime.now())))
                Tasks.remove(trend)


