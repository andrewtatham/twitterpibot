from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.MyQueues as MyQueues
from twitterpibot.twitter import SavedSearches, TwitterHelper


class SavedSearchScheduledTask(ScheduledTask):
    def __init__(self):
        super(SavedSearchScheduledTask, self).__init__()
        self._savedSearches = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=7)

    def onRun(self):
        if not self._savedSearches:
            searches = SavedSearches.get_saved_searches()
            self._savedSearches.extend(searches)

        if self._savedSearches:
            search = self._savedSearches.pop()
            searchTweets = TwitterHelper.search(search)
            for searchTweet in searchTweets:
                searchTweet['tweetsource'] = "search:" + search
                MyQueues.inbox.put(searchTweet)
