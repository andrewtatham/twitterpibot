import logging
import random
import time

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class FollowScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=4)

    def on_run(self):
        list_names = ["Awesome Bots", "Retweet More"]
        for list_name in list_names:
            if list_name in self.identity.lists._sets:
                list_members = self.identity.lists._sets[list_name]
                if list_members and self.identity.following:
                    to_follow = list(list_members.difference(self.identity.following))
                    self._follow_users(to_follow)

        subscriptions = self.identity.twitter.get_list_subscriptions()
        for subscribed_list in subscriptions["lists"]:
            subscribed_list_members = self.identity.twitter.get_list_members(list_id=subscribed_list["id_str"])

            ids = set(map(lambda usr: usr["id_str"], subscribed_list_members["users"]))
            to_follow = ids.difference(self.identity.following)
            self._follow_users(to_follow)

    def _follow_users(self, to_follow):
        if to_follow:
            for user_id in list(to_follow)[:20]:
                self._follow(user_id)

    def _follow(self, user_id):
        logger.info("Following user id %s" % user_id)
        self.identity.twitter.follow(user_id=user_id)
        self.identity.following.add(user_id)
        time.sleep(random.randint(1, 3))
