import logging
import os
import pprint
import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import wikipediahelper, fsh
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

logger = logging.getLogger(__name__)


def _cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


class WikipediaScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(24, 48), minutes=random.randint(0, 59))

    def on_run(self):
        file_paths = None
        try:
            page = wikipediahelper.get_random_page()
            if page:
                logging.info(page.title)
                logging.info(page.url)
                logging.info(page.summary)

                text = _cap(page.summary, 140 * 5 - 24)
                file_paths, valid_file_paths = self._get_valid_images(page)
                self.identity.twitter.send(OutgoingTweet(text=text + " " + page.url, file_paths=valid_file_paths))

                if self.identity.facebook:
                    picture = None
                    if page.images:
                        picture = page.images[0]
                    attachment = self.identity.facebook.create_attachment(
                        page.title,
                        page.url,
                        page.url,
                        text,
                        picture)

                    self.identity.facebook.create_wall_post(post_text=text, attachment=attachment)

        finally:
            if file_paths:
                fsh.delete_files(file_paths)

    def _get_valid_images(self, page):
        max_image_size = self.identity.twitter.twitter_configuration["photo_size_limit"]
        file_paths = None
        valid_file_paths = None
        folder = fsh.root + "temp" + os.sep + "wikipedia" + os.sep + self.identity.screen_name + os.sep
        fsh.ensure_directory_exists(folder)
        if any(page.images):
            logger.info(pprint.pformat(page.images))
            images = list(filter(lambda url: fsh.check_extension(url), page.images))
            if any(images):
                logger.info(pprint.pformat(images))
                file_paths = list(map(lambda url: fsh.download_file(folder, url), images))
                valid_file_paths = list(filter(lambda path: 0 < fsh.get_file_size(path) <= max_image_size, file_paths))
                if any(valid_file_paths):
                    valid_file_paths.sort(key=lambda path: fsh.get_file_size(path))
                    valid_file_paths.reverse()
                    logger.info(pprint.pformat(valid_file_paths))
        return file_paths, valid_file_paths


if __name__ == "__main__":
    import identities_pis

    logging.basicConfig(level=logging.INFO)
    identity = identities_pis.AndrewTathamPiIdentity()
    task = WikipediaScheduledTask(identity)
    for i in range(1):
        task.on_run()
