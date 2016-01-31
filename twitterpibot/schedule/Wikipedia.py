import logging
import os
import random

from apscheduler.triggers.cron import CronTrigger
import requests
import wikipedia

from wikipedia.exceptions import DisambiguationError, PageError

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


def cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


logger = logging.getLogger(__name__)
folder = "temp" + os.sep + "wikipedia" + os.sep

if not os.path.exists(folder):
    logger.info("Creating " + folder)
    os.makedirs(folder)


def download_file(url):
    local_filename = folder + url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return local_filename


class Wikipedia(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*")

    def onRun(self):
        # https://wikipedia.readthedocs.org/en/latest/quickstart.html
        rand = wikipedia.random(pages=1)
        page = None
        while not page:
            try:
                page = wikipedia.page(title=rand)
            except PageError:
                rand = wikipedia.random(pages=1)
                page = None
            except DisambiguationError as e:
                rand = random.choice(e.options)
                page = None

        if page:
            text = cap(page.summary, 100) + page.url
            file_paths = None
            if any(page.images):
                url = page.images[0]
                file_paths = [download_file(url)]

            send(OutgoingTweet(text=text, file_paths=file_paths))
