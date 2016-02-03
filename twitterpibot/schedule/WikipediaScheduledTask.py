import logging
import os
import pprint
import random
import textwrap

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


def tweet_random_wikipedia_page():
    page = WikipediaWrapper.get_random_page()
    if page:

        text = cap(page.url + " " + page.summary, 140)

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


def tweet_random_misconception():
    reply_to_id = None
    misconception = WikipediaWrapper.get_random_misconception()
    lines = textwrap.wrap(misconception, 140 - 6)
    lines_count = len(lines)
    line_number = 0

    for line in lines:
        is_continuation = lines_count > 1 and line_number != 0
        has_continuation = lines_count > 1 and line_number != lines_count - 1
        text = ""
        if is_continuation:
            text += "..."
        text += line
        if has_continuation:
            text += "..."
        reply_to_id = send(OutgoingTweet(text=text, in_reply_to_status_id=reply_to_id))
        line_number += 1


class WikipediaScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="*", minute="15,45")

    def onRun(self):
        if random.randint(0, 1) == 0:
            tweet_random_misconception()
        else:
            tweet_random_wikipedia_page()


if __name__ == "__main__":
    os.chdir("../../")
    task = WikipediaScheduledTask()
    task.onRun()
