import logging
import random

from apscheduler.triggers.interval import IntervalTrigger

import identities
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.users.lists import default_lists

logger = logging.getLogger(__name__)


class UserListsScheduledTask(ScheduledTask):
    def __init__(self, identity, master_identity):
        ScheduledTask.__init__(self, identity)
        self._master_identity = master_identity

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        self.synchronize_lists()

    def synchronize_lists(self):
        self.identity.users.lists.update_lists()

        if self._master_identity:
            self._synchronize([self.identity, self._master_identity])
        else:
            self._add_following_to_list("Need Input")

    def _synchronize(self, identities):

        for user_list in default_lists:
            logger.info("Synchronizing " + user_list)

            master_list = set()
            for identity in identities:
                master_list.update(identity.users.lists._sets[user_list])

            for identity in identities:
                self._add_missing_users(identity, user_list, master_list)

    def _add_missing_users(self, identity, user_list, master_list):
        missing_users = master_list.difference(identity.users.lists._sets[user_list])
        if missing_users:
            for missing_user in missing_users:
                logger.info("adding " + missing_user + " to " + identity.screen_name + " " + user_list)
                identity.users.lists.add_user_to_list(user_list, user_id=missing_user, screen_name=None)

    def _add_following_to_list(self, user_list):
        to_add = self.identity.users._following.difference(self.identity.users.lists._sets[user_list])
        if to_add:
            for missing_user in random.sample(to_add, 1):
                logger.info("adding " + missing_user + " to " + self.identity.screen_name + " " + user_list)
                self.identity.users.lists.add_user_to_list(user_list, user_id=missing_user, screen_name=None)


if __name__ == '__main__':
    import identities_pis

    logging.basicConfig(level=logging.INFO)
    identity = identities.AndrewTathamIdentity()
    task = UserListsScheduledTask(identity, None)
    for _ in range(3):
        task.on_run()
