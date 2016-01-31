import logging
import os
import pprint

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import WikipediaWrapper, FileSystemHelper
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter import TwitterHelper
from twitterpibot.twitter.TwitterHelper import send

link = 21
space = 1
ellipsis = 3
length = 140-(link + space + ellipsis)

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
            text = cap(page.url + " " + cap(page.summary, length), 140)
            file_paths = None
            if any(page.images):
                # filter to PNG, JPEG, WEBP and GIF.
                images = list(filter(lambda url: FileSystemHelper.check_extension(url), page.images))
                if any(images):
                    pprint.pprint(images)
                    url = images[0]
                    path = FileSystemHelper.download_file(folder, url)
                    file_paths = [path]

            send(OutgoingTweet(text=text, file_paths=file_paths))


if __name__ == "__main__":
    os.chdir("../../")
    task = WikipediaScheduledTask()
    task.onRun()
