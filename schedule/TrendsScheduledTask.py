from ScheduledTask import ScheduledTask
from colorama import Fore, Style
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter
from Queue import Queue
from apscheduler.triggers.cron import CronTrigger
import urllib
from collections import Counter
from OutgoingTweet import OutgoingTweet


worldwide_WOEID = 1
UK_WOEID = 23424975
leeds_WOEID = 26042

trendColours = cycle([Fore.MAGENTA, Fore.WHITE])

class TrendsScheduledTask(ScheduledTask):
    def __init__(self, *args, **kwargs):
        self._trendsList = Queue()

    def GetTrigger(args):
        return IntervalTrigger(minutes=29)

    def UpdateTrends(args, twitter):
        print("Updating trends")
        
        #availtrends = twitter.get_available_trends()
        #worldwide_trends = twitter.get_place_trends(id = worldwide_WOEID)
        uk_trends = twitter.get_place_trends(id = UK_WOEID)
        leeds_trends = twitter.get_place_trends(id = leeds_WOEID)
        
        trends = set()
        #for trend in worldwide_trends[0].get('trends',[]):
        #    trends.add(trend['name'])
        for trend in uk_trends[0].get('trends',[]):
            trends.add(trend['name'])
        for trend in leeds_trends[0].get('trends',[]):
            trends.add(trend['name'])
    
        for trend in trends:
            colour = trendColours.next()
            print(colour + "Trends: [" + trend + "]")
            args._trendsList.put(trend)


    def onRun(args):
        with MyTwitter() as twitter:


            if args._trendsList.empty():
                args.UpdateTrends(twitter)
            try:
                trend = args._trendsList.get()
                trendtweets = twitter.search(q = urllib.quote_plus(trend), result_type = "popular")

                trendText = ""
                for trendtweet in trendtweets["statuses"]:
                    colour = trendColours.next()
                    trendText += " " + trendtweet["text"].replace("\n", "   ")
                    print(colour + "Trend: [" + trend + "] - " \
                        + trendtweet["user"]["name"] + " [@" + trendtweet["user"]["screen_name"] + "] - "\
                        + trendtweet["text"].replace("\n", "   "))

                words = trendText.split()
                word_counts = Counter(words)
                
                text = ""
                for word_count in word_counts:
                    text += word_count + " "
                if text:
                    args.context.outbox.put(OutgoingTweet(text=text[:140]))

            finally:
                args._trendsList.task_done()

    