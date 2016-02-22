from itertools import cycle
import logging
import os
import pprint
import textwrap

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import WikipediaWrapper, FileSystemHelper
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet


def cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


logger = logging.getLogger(__name__)
folder = FileSystemHelper.root + "temp" + os.sep + "wikipedia" + os.sep

FileSystemHelper.ensure_directory_exists(folder)


def _split_text(large_text):
    lines = textwrap.wrap(large_text, 140 - 6)
    lines_count = len(lines)
    line_number = 0
    return_value = []
    for line in lines:
        is_continuation = lines_count > 1 and line_number != 0
        has_continuation = lines_count > 1 and line_number != lines_count - 1
        text = ""
        if is_continuation:
            text += "..."
        text += line
        if has_continuation:
            text += "..."
        return_value.append(text)
        line_number += 1
    return return_value


def _tweet_page(identity, page):
    if page:
        lines = _split_text(cap(page.url + " " + page.summary, 140 * 5))
        line_number = 0
        reply_to_id = None
        file_paths = None
        if any(page.images):
            logger.info(pprint.pformat(page.images))
            images = list(filter(lambda url: FileSystemHelper.check_extension(url), page.images))
            if any(images):
                logger.info(pprint.pformat(images))
                file_paths = list(map(lambda url: FileSystemHelper.download_file(folder, url), images[:4]))
                logger.info(pprint.pformat(file_paths))
        for line in lines:
            logger.info(line)
            if line_number == 0 and file_paths:
                reply_to_id = identity.twitter.send(OutgoingTweet(
                    text=line,
                    file_paths=file_paths,
                    in_reply_to_status_id=reply_to_id))
            else:
                reply_to_id = identity.twitter.send(OutgoingTweet(
                    text=line,
                    in_reply_to_status_id=reply_to_id))
            line_number += 1
            FileSystemHelper.delete_files(file_paths)


def _tweet_text(identity, misconception):
    reply_to_id = None
    lines = _split_text(misconception)
    for line in lines:
        reply_to_id = identity.twitter.send(OutgoingTweet(text=line, in_reply_to_status_id=reply_to_id))


def tweet_random_wikipedia_page(identity):
    _tweet_page(identity, WikipediaWrapper.get_random_page())


def tweet_random_misconception(identity):
    _tweet_text(identity, WikipediaWrapper.get_random_misconception())


def tweet_random_python_fact(identity):
    _tweet_text(identity, WikipediaWrapper.get_random_python_fact())


funcs = cycle([
    tweet_random_wikipedia_page,
    tweet_random_misconception,
    # tweet_random_python_fact
])


class WikipediaScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="*/3", minute="15,45")

    def on_run(self):
        func = next(funcs)
        func(self.identity)


if __name__ == "__main__":
    os.chdir("../../")
    logging.basicConfig(level=logging.INFO)
    task = WikipediaScheduledTask(None)
    for i in range(3):
        task.on_run()
