from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.MyQueues as MyQueues


class SavedSearchScheduledTask(ScheduledTask):
    def __init__(self):
        super(SavedSearchScheduledTask, self).__init__(self.identity)
        self._savedSearches = []

    def get_trigger(self):
        return IntervalTrigger(minutes=7)

    def on_run(self):
        if not self._savedSearches:
            searches = self.identity.savedsearches.get_saved_searches()
            self._savedSearches.extend(searches)

        if self._savedSearches:
            search = self._savedSearches.pop()
            search_tweets = self.identity.twitter.search(search)
            for search_tweet in search_tweets:
                search_tweet['tweet_source'] = "search:" + search
                MyQueues.inbox.put(search_tweet)
