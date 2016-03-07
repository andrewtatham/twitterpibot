import logging
import random
import time

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class FollowScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(FollowScheduledTask, self).__init__(identity)
        self.to_follow = []

    def get_trigger(self):
        return IntervalTrigger(minutes=16)

    def _get_unfollowed_list_members(self, list_names):
        to_follow = set()
        for list_name in list_names:
            if list_name in self.identity.lists._sets:
                list_members = self.identity.lists._sets[list_name]
                if list_members and self.identity.following:
                    to_follow.update(list_members.difference(self.identity.following))
        return to_follow

    def _get_unfollowed_subscribed_list_members(self):
        to_follow = set()
        subscriptions = self.identity.twitter.get_list_subscriptions()
        for subscribed_list in subscriptions["lists"]:
            subscribed_list_members = self.identity.twitter.get_list_members(list_id=subscribed_list["id_str"])
            ids = set(map(lambda usr: usr["id_str"], subscribed_list_members["users"]))
            if ids and self.identity.following:
                to_follow.update(ids.difference(self.identity.following))
        return to_follow

    def on_run(self):

        if not self.to_follow:
            to_follow = set()
            to_follow.update(self._get_unfollowed_list_members(list_names=["Friends", "Awesome Bots", "Retweet More"]))
            to_follow.update(self._get_unfollowed_subscribed_list_members())
            self.to_follow = list(to_follow)
            logger.info("To follow %s users" % len(self.to_follow))
            random.shuffle(self.to_follow)

        if self.to_follow:
            for i in range(random.randint(5, 10)):
                if self.to_follow:
                    self._follow(self.to_follow.pop())

    def _follow(self, user_id):
        logger.info("Following user id %s" % user_id)
        self.identity.twitter.follow(user_id=user_id)
        self.identity.following.add(user_id)
        time.sleep(random.randint(1, 3))
