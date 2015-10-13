from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
import random
import MyQueues

class SavedSearchScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self._savedSearches = []

    def GetTrigger(args):
        return IntervalTrigger(minutes=32)

    def onRun(args):
        with MyTwitter() as twitter:
            if not args._savedSearches:
                searches = twitter.get_saved_searches()
                args._savedSearches.extend(searches)

            search = args._savedSearches.pop()
            searchTweets = twitter.search(q = search['query'])
            for searchTweet in searchTweets["statuses"]:
                searchTweet['tweetsource'] = "search:" + search["name"]
                MyQueues.inbox.put(searchTweet)
