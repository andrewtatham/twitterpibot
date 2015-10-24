from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
import random
import MyQueues

class SavedSearchScheduledTask(ScheduledTask):
    def __init__(self):
        self._savedSearches = []

    def GetTrigger(self):
        return IntervalTrigger(minutes=32)

    def onRun(self):
        with MyTwitter() as twitter:
            if not self._savedSearches:
                searches = twitter.get_saved_searches()
                self._savedSearches.extend(searches)

            if self._savedSearches:
                search = self._savedSearches.pop()
                searchTweets = twitter.search(q = search['query'])
                for searchTweet in searchTweets["statuses"]:
                    searchTweet['tweetsource'] = "search:" + search["name"]
                    MyQueues.inbox.put(searchTweet)
