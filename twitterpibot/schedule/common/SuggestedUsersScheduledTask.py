import logging
import random
from itertools import cycle

from apscheduler.triggers.interval import IntervalTrigger
from colorama import Fore

from twitterpibot.schedule.ScheduledTask import ScheduledTask
logger = logging.getLogger(__name__)
# import random

suggestedUserColours = cycle([Fore.WHITE, Fore.CYAN])

ignored_slugs = {
    # "Government", "London Services", "Sport", "Premier League", "Television", "Fashion"
}


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
                    logger.debug(category)
                    colour = next(suggestedUserColours)
                    logger.info(colour + "Users: [" + category["name"] + "]")
                    self._slug_list.append(category)
            self._slug_list.reverse()

        category = self._slug_list.pop()
        suggested_users = self.identity.twitter.get_user_suggestions_by_slug(slug=category["slug"])["users"]

        for user_data in suggested_users:
            colour = next(suggestedUserColours)
            # user cache will be populated with suggested users
            user = self.identity.users.get_user(user_data=user_data)
            if user:
                logger.info(colour + "User: [" + category["name"] + "] - " + user.long_description())

                if not self.identity.users.lists.list_contains_user("Need Input", user):
                    self.identity.users.lists.add_user_to_list(
                        list_name="Need Input",
                        user_id=user.id_str,
                        screen_name=user.screen_name)


if __name__ == '__main__':
    import identities_pis

    logging.basicConfig(level=logging.INFO)
    identity = identities_pis.AndrewTathamPi2Identity(None)
    task = SuggestedUsersScheduledTask(identity)
    for _ in range(3):
        task.on_run()
