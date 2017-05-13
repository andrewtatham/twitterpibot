import datetime
import random

from apscheduler.triggers.interval import IntervalTrigger
import logging

import identities_pis
from twitterpibot.logic.conversation import attention_words, human_words
from twitterpibot.logic.phrase_generator import generate_phrase, phrase_wrap_list
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet


class Announcement(object):
    def __init__(self, message,
                 duration_days=30,
                 twitter=True,
                 facebook=True,
                 link=None,
                 date_added=None):
        if not date_added:
            date_added = datetime.datetime.utcnow()

        self._message = message
        self._expires = date_added + datetime.timedelta(days=duration_days)
        self.twitter = twitter
        self.facebook = facebook
        self.link = link

    def message(self):
        return generate_phrase(self._message)

    def is_expired(self):
        return datetime.datetime.utcnow() > self._expires


class AnnouncementScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(AnnouncementScheduledTask, self).__init__(identity)

        attention_humans = "{} {} ".format(phrase_wrap_list(attention_words),
                                           phrase_wrap_list(human_words))

        facebook_announcement = Announcement(
            attention_humans + "we (iz|are) now (in|on|up in ur) facebook",
            link="https://www.facebook.com/andrewtathampi",
            facebook=False,
            date_added=datetime.datetime(2016, 9, 24))

        self._announcements_master = [
            facebook_announcement
        ]
        self._announcements = []

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(2, 5), minutes=random.randint(0, 59))

    def on_run(self):
        if not self._announcements and self._announcements_master:
            self._remove_expired()
            if self._announcements_master:
                self._announcements = list(self._announcements_master)

        if self._announcements:
            announcement = self._announcements.pop()
            if announcement:
                message = announcement.message()
                if self.identity.twitter and announcement.twitter:
                    twitter_text = message
                    if announcement.link:
                        twitter_text += " " + announcement.link

                    self.identity.twitter.send(OutgoingTweet(text=twitter_text))

                if self.identity.facebook and announcement.facebook:
                    attachment = None
                    if announcement.link:
                        attachment = self.identity.facebook.create_attachment(
                            link=announcement.link
                        )
                    self.identity.facebook.create_wall_post(message, attachment)

    def _remove_expired(self):
        if any(self._announcements_master):
            expired = list(filter(lambda a: a.is_expired(), self._announcements_master))
            if expired:
                for e in expired:
                    self._announcements_master.remove(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    identity = identities_pis.AndrewTathamPiIdentity(None)
    task = AnnouncementScheduledTask(identity)
    task.on_run()
