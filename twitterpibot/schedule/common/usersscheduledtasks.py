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
        self.to_unfollow = []
        self.to_block = []
        self.to_report = []

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))
        # return IntervalTrigger(minutes=3)

    def _get_unfollowed_list_members(self, list_names):
        to_follow = set()
        for list_name in list_names:
            if list_name in self.identity.users._lists._sets:
                list_members = self.identity.users._lists._sets[list_name]
                if list_members and self.identity.users._following:
                    to_follow.update(list_members.difference(self.identity.users._following))
        return to_follow

    def _get_subscribed_list_members(self):
        members = set()
        subscriptions = self.identity.twitter.get_list_subscriptions()
        for subscribed_list in subscriptions["lists"]:
            subscribed_list_members = self.identity.twitter.get_list_members(list_id=subscribed_list["id_str"])
            ids = set(map(lambda usr: usr["id_str"], subscribed_list_members["users"]))
            members.update(ids)
        return members

    def _get_followed_subscribed_list_members(self):
        followed = set()
        members = self._get_subscribed_list_members()
        if members and self.identity.users._following:
            followed.update(members.intersection(self.identity.users._following))
        return followed

    def _get_unfollowed_subscribed_list_members(self):
        unfollowed = set()
        members = self._get_subscribed_list_members()
        if members and self.identity.users._following:
            unfollowed.update(members.difference(self.identity.users._following))
        return unfollowed

    def _get_to_follow(self):
        to_follow = set()
        # todo get high scoring users and follow
        # to_follow.update(
        #     self._get_unfollowed_list_members(list_names=["Friends", "Awesome Bots", "Retweet More"]))
        # to_follow.update(self._get_unfollowed_subscribed_list_members())
        to_follow = list(to_follow)
        logger.info("To follow %s users" % len(to_follow))
        random.shuffle(to_follow)
        return to_follow

    def _get_to_unfollow(self):
        to_unfollow = set()

        to_unfollow.update(self._get_followed_subscribed_list_members())
        # todo unfollow
        # inactive > 1 year
        # japanese/non english

        to_unfollow = list(to_unfollow)
        logger.info("To unfollow %s users" % len(to_unfollow))
        random.shuffle(to_unfollow)
        return to_unfollow

    def on_run(self):
        self._unfollow()
        # todo block/report
        # smut spam bots
        # biz spam bots

        self._follow()

    def _follow(self):
        can_follow = len(self.identity.users._followers) < 4500
        if can_follow:
            if not self.to_follow:
                self.to_follow = self._get_to_follow()

            if self.to_follow:
                for i in range(random.randint(1, 10)):
                    if self.to_follow:
                        user_id = self.to_follow.pop()
                        user = self.identity.users.get_user(user_id=user_id)
                        if user and not user.is_me and not user.follow_request_sent:
                            self.identity.users.follow(user_id=user_id)

    def _unfollow(self):
        if not self.to_unfollow:
            self.to_unfollow = self._get_to_unfollow()
        if self.to_unfollow:
            for i in range(random.randint(1, 10)):
                if self.to_unfollow:
                    self.identity.users.unfollow(user_id=self.to_unfollow.pop())


class GetUsersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(GetUsersScheduledTask, self).__init__(identity)
        self._all_user_ids = []

    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(5, 7))

    def on_run(self):
        if not self._all_user_ids:
            all_user_ids = set()
            all_user_ids.update(self.identity.users.get_following())
            all_user_ids.update(self.identity.users.get_followers())
            all_user_ids = list(all_user_ids)
            random.shuffle(all_user_ids)
            self._all_user_ids = all_user_ids

        if self._all_user_ids:
            number = self.identity.twitter.rates.get("/users/lookup")
            number = int(number * 25)  # 100 users per call, but only use 1/4 allowance
            batch = []
            for _ in range(number):
                if self._all_user_ids:
                    batch.append(self._all_user_ids.pop())
                else:
                    break
            # get user data, so users who dont tweet are cached
            self.identity.users.get_users(batch)


class ScoreUsersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ScoreUsersScheduledTask, self).__init__(identity)
        self._all_user_ids = []

    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(5, 7))

    def on_run(self):
        nummber = self.identity.twitter.rates.get("/statuses/user_timeline")

        no_of_scores = self.identity.users.score_users(nummber)
        # if no_of_scores > 10:
        #     self.identity.users.get_leaderboard(10)
