import logging

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class UserListsScheduledTask(ScheduledTask):
    def __init__(self, master_identity, lists):
        ScheduledTask.__init__(self, master_identity)
        self._lists = lists

    def get_trigger(self):
        return IntervalTrigger(hours=2)

    def on_run(self):
        self.synchronize_lists()

    def synchronize_lists(self):
        self.identity.lists.update_lists()
        if self.identity.slave_identities:
            for identity in self.identity.slave_identities:
                identity.lists.update_lists()

            for user_list in self._lists:
                logger.info("Synchronizing " + user_list)
                master_list = set()
                for identity in self.identity.slave_identities:
                    master_list = master_list.union(identity.lists._sets[user_list])

                for identity in self.identity.slave_identities:
                    missing_users = master_list.difference(identity.lists._sets[user_list])
                    if missing_users:
                        for missing_user in missing_users:
                            logger.info("adding " + missing_user + " to " + identity.screen_name + " " + user_list)
                            identity.lists.add_user(user_list, user_id=missing_user, screen_name=None)
