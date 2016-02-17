import logging

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class UserListsScheduledTask(ScheduledTask):
    def __init__(self, identities, lists):
        ScheduledTask.__init__(self, identities[0])
        self.identities = identities
        self.lists = lists

    def get_trigger(self):
        return IntervalTrigger(hours=2)

    def on_run(self):

        for identity in self.identities:
            identity.lists.update_lists()

        for user_list in self.lists:
            logger.info("Syncronizing " + user_list)
            master_list = set()
            for identity in self.identities:
                master_list = master_list.union(identity.lists._sets[user_list])

            for identity in self.identities:
                missing_users = master_list - identity.lists._sets[user_list]
                if missing_users:
                    for missing_user in missing_users:
                        logger.info("adding " + missing_user + " to " + identity.screen_name + " " + user_list)
                        identity.lists.add_user(user_list, user_id=missing_user, screen_name=None)
