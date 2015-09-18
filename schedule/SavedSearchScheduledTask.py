from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
from colorama import Fore
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from Queue import Queue
import random

searchColours = cycle([Fore.BLUE, Fore.WHITE])

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
                    colour = searchColours.next()
                    print(colour + "SavedSearches: [" + search['name'] + "]")
                    args._savedSearches.put(search)
            try:
                search = args._savedSearches.get()
                searchTweets = twitter.search(q = search['query'])
                for searchTweet in searchTweets["statuses"]:
                    colour = searchColours.next()                    
                    print(colour + "SavedSearch: [" + search['name'] + "] - " \
                        + searchTweet["user"]["name"] + " [@" + searchTweet["user"]["screen_name"] + "] - "\
                        + searchTweet["text"].replace("\n", "   "))

                searchTweet = random.choice(searchTweets["statuses"])
                twitter.retweet(id = searchTweet["id_str"])

                # TODO reply?
            finally:
                args._savedSearches.task_done()

