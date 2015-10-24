import random

from apscheduler.triggers.cron import CronTrigger

from ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
import wikipedia
from wikipedia.exceptions import DisambiguationError
from twitterpibot.twitter.TwitterHelper import Send


class Wikipedia(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*")

    def onRun(self):

        # https://wikipedia.readthedocs.org/en/latest/quickstart.html

        isDisambiguation = True
        rand = wikipedia.random(pages=1)
        page = None
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
