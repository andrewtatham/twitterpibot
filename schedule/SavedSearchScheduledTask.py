from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from Queue import Queue
import random


class SavedSearchScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self._savedSearches = Queue()

    def GetTrigger(args):
        return IntervalTrigger(minutes=32)

    def onRun(args):
        with MyTwitter() as twitter:
            if args._savedSearches.empty():
                searches = twitter.get_saved_searches()
                for search in searches:
                    args._savedSearches.put(search)
            try:
                search = args._savedSearches.get()
                searchTweets = twitter.search(q = search['query'])
                for searchTweet in searchTweets["statuses"]:
                    searchTweet['tweetsource'] = "search:" + search["name"]
                    args.context.inbox.put(searchTweet)

            finally:
                args._savedSearches.task_done()

