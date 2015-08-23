from ScheduledTask import ScheduledTask
from colorama import Fore, Style
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter
from Queue import Queue
from apscheduler.triggers.cron import CronTrigger
import urllib


worldwide_WOEID = 1
leeds_WOEID = 26042

trendColours = cycle([Fore.MAGENTA, Fore.CYAN])

class TrendsScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):

        self._trendsList = Queue()




    def GetTrigger(args):
        return IntervalTrigger(minutes=5)



    def UpdateTrends(args, twitter):
        print("Updating trends")
        
        #availtrends = twitter.get_available_trends()
        worldwide_trends = twitter.get_place_trends(id = worldwide_WOEID)
        leeds_trends = twitter.get_place_trends(id = leeds_WOEID)
        
        trends = set()
        for trend in worldwide_trends[0].get('trends',[]):
            trends.add(trend['name'])
        for trend in leeds_trends[0].get('trends',[]):
            trends.add(trend['name'])
    
        for trend in trends:
            colour = trendColours.next()
            print("T: [" + trend + "]")
            args._trendsList.put(trend)


    def onRun(args):
        with MyTwitter() as twitter:


            if args._trendsList.empty():
                args.UpdateTrends(twitter)
            try:
                trend = args._trendsList.get()
                trendtweets = twitter.search(q = urllib.quote_plus(trend), result_type = "popular")
                for trendtweet in trendtweets["statuses"]:
                    colour = trendColours.next()
                    print("T: [" + trend + "] - " + trendtweet["text"].replace("\n", "   "))



            finally:
                args._trendsList.task_done()

    