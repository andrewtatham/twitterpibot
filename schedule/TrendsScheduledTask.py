from ScheduledTask import ScheduledTask
from colorama import Fore, Style
from itertools import cycle
from apscheduler.triggers.interval import IntervalTrigger
from MyTwitter import MyTwitter

worldwide_WOEID = 1
leeds_WOEID = 26042

trendColours = cycle([Fore.MAGENTA, Fore.CYAN])

class TrendsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return IntervalTrigger(hours=2)



    def onRun(args):
        with MyTwitter() as twitter:
            #availtrends = twitter.get_available_trends()
            worldwide_trends = twitter.get_place_trends(id = worldwide_WOEID)
            args.printTrends('Worldwide Trends', worldwide_trends)
    
            leeds_trends = twitter.get_place_trends(id = leeds_WOEID)
            args.printTrends('Leeds Trends', leeds_trends)

    def printTrends(args, title, trends):

        displaytrends = []

        for trend in trends[0]["trends"]:
            trendname = trend["name"]
            displaytrends.append(trendname)

        #for trend in trends:
        #    trendtweets = args.context.twitter.search(q = urllib.quote_plus(trend), result_type = "popular")
        #    for trendtweet in trendtweets["statuses"]:
        #        print("  " + trendtweet["text"].replace("\n", "   "))

        colour = trendColours.next()

        print("")
        print (Style.BRIGHT + colour + str(title))
        for trend in displaytrends:
        
            print (Style.NORMAL + colour + str(trend))
            print("")     