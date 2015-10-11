from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
import wikipedia
from wikipedia.wikipedia import WikipediaPage
from wikipedia.exceptions import DisambiguationError
import random

class Wikipedia(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour="*")
    

    def onRun(args):

        # https://wikipedia.readthedocs.org/en/latest/quickstart.html

        isDisambiguation = True
        rand = wikipedia.random(pages=1)
        while isDisambiguation:
            try:
                page = wikipedia.page(title=rand)
                isDisambiguation = False
            except DisambiguationError as e:
                rand = random.choice(e.options)
                isDisambiguation = True


        if page:

            
            text = cap(page.summary, 100) + page.url
            tweet = OutgoingTweet(text=text)
            Send(tweet)

def cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'