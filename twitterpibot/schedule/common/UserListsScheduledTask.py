import logging
import random

from apscheduler.triggers.interval import IntervalTrigger

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
        self.identity.lists.update_lists()

        if self._master_identity:
            self._synchronize([self.identity, self._master_identity])

    def _synchronize(self, identities):

        for user_list in default_lists:
            logger.info("Synchronizing " + user_list)

            master_list = set()
            for identity in identities:
                master_list.update(identity.lists._sets[user_list])

            for identity in identities:
                self._add_missing_users(identity, user_list, master_list)

    def _add_missing_users(self, identity, user_list, master_list):
        missing_users = master_list.difference(identity.lists._sets[user_list])
        if missing_users:
            for missing_user in missing_users:
                logger.info("adding " + missing_user + " to " + identity.screen_name + " " + user_list)
                identity.lists.add_user(user_list, user_id=missing_user, screen_name=None)
