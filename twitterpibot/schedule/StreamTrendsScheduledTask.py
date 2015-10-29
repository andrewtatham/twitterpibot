import datetime

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
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
        # saved_list = SavedSearches.get_saved_searches()
        trends_list = TrendingTopics.get()
        stream_list = Tasks.get()

        # Check for streams that are no longer trending
        for trend in stream_list:

            # is_one_direction = OneDirection.is_one_direction(trend)
            # is_saved = trend in saved_list
            is_trending = trend in trends_list

            if not is_trending:
                # stop stream
                Send(OutgoingDirectMessage(text="Stopping stream " + trend + " " + str(datetime.datetime.now())))
                Tasks.remove(trend)


        # Check for new trends
        new_stream_count = 0
        for trend in trends_list:

            # is_one_direction = OneDirection.is_one_direction(trend)
            # is_saved = trend in saved_list
            is_streaming = trend in stream_list

            if not is_streaming:
                # Create stream
                Tasks.add(StreamTweetsTask(TwitterHelper.GetStreamer(topic=trend)))
                Send(OutgoingDirectMessage(text="Starting stream " + trend + " " + str(datetime.datetime.now())))
                new_stream_count += 1

                if new_stream_count >= 4:
                    break




