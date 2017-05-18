import logging
import random
from time import sleep

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)

_auto_follow_lists = ["Friends", "Awesome Bots", "Retweet More"]


class ManageUsersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ManageUsersScheduledTask, self).__init__(identity)
        self.to_follow_set = {}
        self.to_follow_list = []
        self.to_unfollow_set = {}
        self.to_unfollow_list = []
        self.to_block = []
        self.to_report = []

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))
        # return IntervalTrigger(minutes=3)

    def _get_to_follow(self):
        to_follow = set()
        # todo get high scoring users and follow
        to_follow.update(self.identity.users.get_unfollowed_list_members(list_names=_auto_follow_lists))
        return to_follow

    def _get_to_unfollow(self):
        to_unfollow = set()
        to_unfollow.update(self.identity.users.get_followed_inactive())
        return to_unfollow

    def _get_to_not_unfollow(self):
        to_unfollow = set()
        to_unfollow.update(self.identity.users.get_followed_list_members(list_names=_auto_follow_lists))
        return to_unfollow

    @staticmethod
    def _set_to_shuffled_list(a_set):
        a_list = list(a_set)
        random.shuffle(a_list)
        return a_list

    def on_run(self):
        # todo block/report
        # smut spam bots
        # biz spam bots

        if not self.to_unfollow_list:
            self.to_unfollow_set = self._get_to_unfollow().difference(self._get_to_not_unfollow())
        if not self.to_follow_list:
            self.to_follow_set = self._get_to_follow()

        if self.to_unfollow_set and not self.to_unfollow_list:
            self.to_unfollow_list = self._set_to_shuffled_list(self.to_unfollow_set)
            logger.info("To unfollow %s users" % len(self.to_unfollow_list))
        if self.to_follow_set and not self.to_follow_list:
            self.to_follow_list = self._set_to_shuffled_list(self.to_follow_set.difference(self.to_unfollow_set))
            logger.info("To follow %s users" % len(self.to_follow_list))

        if self.to_unfollow_list:
            for i in range(random.randint(1, 10)):
                if self.to_unfollow_list:
                    self.identity.users.unfollow(user_id=self.to_unfollow_list.pop())

        can_follow = len(self.identity.users._followers) < 4500

        if self.to_follow_list and can_follow:
            for i in range(random.randint(1, 10)):
                if self.to_follow_list:
                    user_id = self.to_follow_list.pop()
                    user = self.identity.users.get_user(user_id=user_id)
                    if user and not user.is_me and not user.follow_request_sent:
                        self.identity.users.follow(user_id=user_id)


class UpdateUserGroupsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(45, 60))

    def on_run(self):
        self.identity.users.get_followers(force=True)
        self.identity.users.get_following(force=True)

        self.identity.users.get_following_followers(force=True)
        self.identity.users.get_following_only(force=True)
        self.identity.users.get_followers_only(force=True)
        self.identity.users.get_others(force=True)


class GetUsersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(GetUsersScheduledTask, self).__init__(identity)
        self._all_user_ids = []

    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(15, 60))

    def on_run(self):
        if not self._all_user_ids:
            self._all_user_ids = self.identity.users.get_uncached_user_ids()

        if self._all_user_ids:
            logger.info("{} uncached user ids".format(len(self._all_user_ids)))
            calls_remaining = self.identity.twitter.rates.get("/users/lookup")
            batch_size = int(calls_remaining / 10)
            batch = []
            for _ in range(batch_size):
                if self._all_user_ids:
                    batch.append(self._all_user_ids.pop())
                else:
                    break

            if batch:
                logger.info("getting {} user ids {}".format(len(batch), batch))
                # get user data, so users who dont tweet are cached
                self.identity.users.get_users(batch)


class ScoreUsersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ScoreUsersScheduledTask, self).__init__(identity)
        self._all_user_ids = []

    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(15, 60))

    def on_run(self):
        calls_remaining = self.identity.twitter.rates.get("/statuses/user_timeline")
        batch_size = int(calls_remaining / 10)
        no_of_scores = self.identity.users.score_users(batch_size)
        # if no_of_scores > 10:
        #     self.identity.users.get_leaderboard(10)


class ManageListMembersScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ManageListMembersScheduledTask, self).__init__(identity)
        self._all_user_ids = []

    def get_trigger(self):
        return IntervalTrigger(minutes=random.randint(15, 60))

    def on_run(self):

        if not self._all_user_ids:
            self._all_user_ids = self.identity.users.get_all_user_ids()

        possibly_bots_list_name = "Possibly Bots"
        possibly_bots_list_members = self.identity.users.lists.get_list_members(list_name=possibly_bots_list_name)

        need_input_list_name = "Need Input"
        need_input_list_members = self.identity.users.lists.get_list_members(list_name=need_input_list_name)

        for _ in range(random.randint(2, 10)):
            if self._all_user_ids:
                user_id = self._all_user_ids.pop()
                if user_id:
                    user = self.identity.users.get_user(user_id=user_id)

                    if user and user.is_possibly_bot and user_id not in possibly_bots_list_members:
                        self.identity.users.lists.add_user_to_list(
                            list_name=possibly_bots_list_name,
                            user_id=user_id, screen_name=user.screen_name)

                    if user and user.verified and user.followers_count >= 1000000 and user_id not in need_input_list_members:
                        self.identity.users.lists.add_user_to_list(
                            list_name=need_input_list_name,
                            user_id=user_id, screen_name=user.screen_name)


if __name__ == '__main__':
    import identities_pis

    logging.basicConfig(level=logging.INFO)

    identity = identities_pis.BotgleArtistIdentity(None)

    get_users_task = GetUsersScheduledTask(identity=identity)
    get_users_task.on_run()

    task = ManageListMembersScheduledTask(identity=identity)
    for _ in range(5):
        task.on_run()
        sleep(5)
