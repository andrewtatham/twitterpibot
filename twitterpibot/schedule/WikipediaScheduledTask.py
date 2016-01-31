import logging
import os

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import WikipediaWrapper, FileSystemHelper
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


def cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


logger = logging.getLogger(__name__)
folder = "temp" + os.sep + "wikipedia" + os.sep

FileSystemHelper.ensure_directory_exists(folder)


class WikipediaScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*")

    def onRun(self):
        page = WikipediaWrapper.GetRandomPage()

        if page:
            text = cap(page.summary, 100) + page.url
            file_paths = None
            if any(page.images):
                url = page.images[0]
                path = FileSystemHelper.download_file(folder, url)
                file_paths = [path]

            send(OutgoingTweet(text=text, file_paths=file_paths))
