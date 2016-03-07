import logging
import os
import pprint

from apscheduler.triggers.cron import CronTrigger

import twitterpibot.identities
from twitterpibot.logic import wikipediahelper, filesystemhelper
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

logger = logging.getLogger(__name__)


def _cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


class WikipediaScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour="*/3", minute="15,45")

    def on_run(self):
        folder = filesystemhelper.root + "temp" + os.sep + "wikipedia" + os.sep + self.identity.screen_name + os.sep
        filesystemhelper.ensure_directory_exists(folder)
        page = wikipediahelper.get_random_page()
        if page:
            text = _cap(page.summary, 140 * 5 - 24) + " " + page.url
            logging.info(text)
            file_paths = None
            if any(page.images):
                logger.info(pprint.pformat(page.images))
                images = list(filter(lambda url: filesystemhelper.check_extension(url), page.images))
                if any(images):
                    logger.info(pprint.pformat(images))
                    file_paths = list(map(lambda url: filesystemhelper.download_file(folder, url), images[:4]))
                    logger.info(pprint.pformat(file_paths))
            self.identity.twitter.send(OutgoingTweet(text=text, file_paths=file_paths))
            if file_paths:
                filesystemhelper.delete_files(file_paths)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    task = WikipediaScheduledTask(twitterpibot.identities.andrewtathampi)
    for i in range(1):
        task.on_run()
