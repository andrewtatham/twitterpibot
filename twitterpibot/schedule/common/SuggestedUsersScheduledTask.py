import logging
from itertools import cycle
import random

from apscheduler.triggers.interval import IntervalTrigger
from colorama import Fore

from twitterpibot.schedule.ScheduledTask import ScheduledTask

# import random
from twitterpibot.users.user import User

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])

ignored_slugs = {"Government", "London Services", "Sport", "Premier League", "Television","Fashion"}


class SuggestedUsersScheduledTask(ScheduledTask, ):
    def __init__(self, identity, slugs=None):
        super(SuggestedUsersScheduledTask, self).__init__(identity)
        self._slug_list = []
        self._slugs = slugs

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):

        if not self._slug_list:
            categories = self.identity.twitter.get_user_suggestions()

            for category in categories:
                if category["name"] not in ignored_slugs:
                    logging.debug(category)
                    colour = next(suggestedUserColours)
                    logging.info(colour + "Users: [" + category["name"] + "]")
                    self._slug_list.append(category)
            self._slug_list.reverse()

        category = self._slug_list.pop()
        suggested_users = self.identity.twitter.get_user_suggestions_by_slug(slug=category["slug"])["users"]

        for user_data in suggested_users:
            colour = next(suggestedUserColours)
            user = User(user_data, identity.screen_name)
            logging.info(colour + "User: [" + category["name"] + "] - " + user.long_description())


if __name__ == '__main__':
    import identities

    logging.basicConfig(level=logging.INFO)
    identity = identities.AndrewTathamPi2Identity(None)
    task = SuggestedUsersScheduledTask(identity)

    task.on_run()
