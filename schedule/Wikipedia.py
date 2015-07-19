from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
import wikipedia
from wikipedia.wikipedia import WikipediaPage
from wikipedia.exceptions import DisambiguationError
import random

class Wikipedia(ScheduledTask):

    def onInit(args):


        return super(Wikipedia, args).onInit()


    def GetTrigger(args):
        
  
        #return CronTrigger(second = datetime.datetime.now().second + 5)

        return CronTrigger(hour = '8-22', minute = '*/15')
    

    def onRun(args):

        # https://wikipedia.readthedocs.org/en/latest/quickstart.html


        rand = wikipedia.random(pages=1)
        try:
            page = wikipedia.page(title=rand)
        except DisambiguationError as e:
            page = WikipediaPage(title=random.choice(e.options))


        if page:

            
            text = cap(page.summary, 100) + page.url
            tweet = OutgoingTweet(text=text)
            args.context.outbox.put(tweet)

def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'