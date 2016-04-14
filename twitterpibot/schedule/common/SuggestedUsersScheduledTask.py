import logging
from itertools import cycle
import random

from apscheduler.triggers.interval import IntervalTrigger
from colorama import Fore

from twitterpibot.schedule.ScheduledTask import ScheduledTask

# import random

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])


class SuggestedUsersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(SuggestedUsersScheduledTask, self).__init__(identity)
        self._slugList = []

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):

        if not self._slugList:
            categories = self.identity.twitter.get_user_suggestions()

            for category in categories:
                colour = next(suggestedUserColours)
                logging.info(colour + "Users: [" + category["name"] + "]")
                self._slugList.append(category)

        category = self._slugList.pop()
        suggested_users = self.identity.twitter.get_user_suggestions_by_slug(slug=category["slug"])["users"]
        for user in suggested_users:
            colour = next(suggestedUserColours)
            logging.info(colour + "User: [" + category["name"] + "] - " + user["name"] + " [@" + user[
                "screen_name"] + "] - " + user["description"].replace("\n", "   "))
