import datetime
import logging
import pprint
import random

from twitterpibot.users import lists
from twitterpibot.users.user import User

logger = logging.getLogger(__name__)


class Users(object):
    def __init__(self, identity):
        self._identity = identity
        self._users = {}

        self._following = set()
        self._followers = set()

        self._following_followers = set()
        self._following_only = set()
        self._followers_only = set()
        self._others = set()

        self._lists = lists.Lists(self._identity)

        self._lists.update_lists()
        self.get_followers()
        self.get_following()

    def get_user(self, user_id=None, user_data=None):
        usr = None
        if user_id and user_id in self._users:
            usr = self._users[user_id]
        else:
            # make new user
            if user_id and not user_data:
                logger.debug("looking up user data %s" % user_id)
                user_data = self._identity.twitter.lookup_user(user_id=user_id)[0]
            elif not user_id and user_data:
                user_id = user_data.get("id_str")

            if user_data:
                logger.debug("creating new user %s" % user_id)
                usr = User(user_data, self._identity)
                self._users[user_id] = usr

        if usr and usr.is_stale():
            logger.debug("updating user %s" % user_id)
            self.update_user(user=usr)

        return usr

    def get_users(self, user_ids, lookup=True):
        n_requested_total = len(user_ids)
        logger.debug("getting {} users".format(n_requested_total))
        users = []
        cached = list(filter(lambda u: u in self._users, user_ids))
        to_lookup = list(filter(lambda u: not u in self._users, user_ids))
        n_cached = len(cached)
        n_uncached = len(to_lookup)
        if n_requested_total:
            logger.debug("{} cached user ids {:.0%}".format(n_cached, n_cached / n_requested_total))
            logger.debug("{} uncached user ids {:.0%}".format(n_uncached, n_cached / n_requested_total))

        for user_id in cached:
            users.append(self.get_user(user_id=user_id))

        if lookup and to_lookup:
            n = 100
            for chunk in [to_lookup[i:i + n] for i in range(0, len(to_lookup), n)]:
                ids_csv = ",".join(chunk)
                logger.debug("lookup {} users".format(len(chunk)))
                user_datas = self._identity.twitter.lookup_user(user_id=ids_csv)
                if user_datas:
                    logger.debug("lookup returned {} users".format(len(user_datas)))
                    for user_data in user_datas:
                        users.append(self.get_user(user_data=user_data))

        n_returned_total = len(users)
        if n_requested_total:
            logger.info("requested {} returning {} users {:.0%}".format(
                n_requested_total, n_returned_total, n_returned_total / n_requested_total))
        return users

    def update_user(self, user):

        self._lists.update_user_list_memberships(user)

        user.follower = user.id_str in self._followers
        user.following = user.id_str in self._following

        user.update_flags()
        user.get_user_score()

        user.updated = datetime.datetime.utcnow()

    def friends(self, friends):
        logger.info("[%s] Friends %s" % (self._identity.screen_name, len(friends)))
        self._following = set([str(f) for f in friends])

    def get_following(self, force=False):
        if not self._following or force:
            self._following = self._identity.twitter.get_following()
        logger.info("[%s] following %s" % (self._identity.screen_name, len(self._following)))
        return self._following

    def get_followers(self, force=False):
        if not self._followers or force:
            self._followers = self._identity.twitter.get_followers()
        logger.info("[%s] followers %s" % (self._identity.screen_name, len(self._followers)))
        return self._followers

    def get_following_followers(self, force=False):
        if not self._following_followers or force:
            self._following_followers = self.get_following().intersection(self.get_followers())
        logger.info("[%s] following_followers %s" % (self._identity.screen_name, len(self._following_followers)))
        return self._following_followers

    def get_following_only(self, force=False):
        if not self._following_only or force:
            self._following_only = self.get_following().difference(self.get_followers())
        logger.info("[%s] following_only %s" % (self._identity.screen_name, len(self._following_only)))
        return self._following_only

    def get_followers_only(self, force=False):
        if not self._followers_only or force:
            self._followers_only = self.get_followers().difference(self.get_following())
        logger.info("[%s] followers_only %s" % (self._identity.screen_name, len(self._followers_only)))
        return self._followers_only

    def get_others(self, force=False):
        if not self._others or force:
            self._others = set(self._users).difference(self.get_following().union(self.get_followers()))
        logger.info("[%s] others %s" % (self._identity.screen_name, len(self._others)))
        return self._others

    def get_users_with_scores(self):
        return list(filter(lambda u: u.user_score, list(self._users.values())))

    def get_users_without_scores(self):
        return list(filter(lambda u: not u.user_score, list(self._users.values())))

    def score_users(self, n=None):
        users_without_scores = self.get_users_without_scores()
        random.shuffle(users_without_scores)
        if n:
            users_without_scores = users_without_scores[:n]
        for user in users_without_scores:
            user.get_user_score()

    def get_leaderboard(self, n=3):
        users_with_scores = self.get_users_with_scores()
        users_with_scores.sort(key=lambda u: u.user_score.total())
        worst = users_with_scores[:n]
        best = users_with_scores[-n:]
        logger.info("USER LEADERBOARD")
        logger.info("BEST")
        for best_user in best:
            logger.info(best_user.long_description())
        logger.info("WORST")
        for worst_user in worst:
            logger.info(worst_user.long_description())

    def follow(self, user_id):
        logger.info("following user id %s" % user_id)
        user = self._users.get(user_id)
        if user:
            self._identity.twitter.follow(user_id=user.id_str, screen_name=user.screen_name)
            self._following.add(user_id)

    def unfollow(self, user_id):
        logger.info("unfollowing user id %s" % user_id)
        user = self._users.get(user_id)
        if user:
            self._identity.twitter.unfollow(user_id=user.id_str, screen_name=user.screen_name)
            self._forget_user_id(user_id)

    def block(self, user_id):
        logger.info("blocking user id %s" % user_id)
        user = self._users.get(user_id)
        if user:
            self._identity.twitter.block(user_id=user.id_str, screen_name=user.screen_name)
            self._forget_user_id(user_id)

    def report(self, user_id):
        logger.info("reporting user id %s" % user_id)
        user = self._users.get(user_id)
        if user:
            self._identity.twitter.report(user_id=user.id_str, screen_name=user.screen_name)
            self._forget_user_id(user_id)

    def _forget_user_id(self, user_id):
        if user_id in self._following:
            self._following.remove(user_id)
        if user_id in self._followers:
            self._followers.remove(user_id)
        if user_id in self._users:
            self._users.pop(user_id, None)

    def get_unfollowed_list_members(self, list_names):
        to_follow = set()
        for list_name in list_names:
            if list_name in self._lists._sets:
                list_members = self._lists._sets[list_name]
                if list_members and self._following:
                    to_follow.update(list_members.difference(self._following))
        return to_follow

    def get_subscribed_list_members(self):
        members = set()
        subscriptions = self._identity.twitter.get_list_subscriptions()
        for subscribed_list in subscriptions["lists"]:
            subscribed_list_members = self._identity.twitter.get_list_members(list_id=subscribed_list["id_str"])
            ids = set(map(lambda usr: usr["id_str"], subscribed_list_members["users"]))
            members.update(ids)
        return members

    def get_followed_subscribed_list_members(self):
        followed = set()
        members = self.get_subscribed_list_members()
        if members and self._following:
            followed.update(members.intersection(self._following))
        return followed

    def get_unfollowed_subscribed_list_members(self):
        unfollowed = set()
        members = self.get_subscribed_list_members()
        if members and self._following:
            unfollowed.update(members.difference(self._following))
        return unfollowed

    def get_followed_inactive(self):
        inactive = set([id_str for id_str, user in self._users.items() if user.is_inactive()])
        return self._following.intersection(inactive)

    def get_uncached_user_ids(self):
        all_user_ids = set()
        all_user_ids.update(self.get_following())
        all_user_ids.update(self.get_followers())
        all_user_ids.difference_update(self._users)
        all_user_ids = list(all_user_ids)
        random.shuffle(all_user_ids)
        return all_user_ids

    def _get_user_score_statistics(self, user_list):
        if user_list:
            scores = list(map(lambda u: u.user_score.total(), filter(lambda u: u.user_score, user_list)))
            if scores:
                scores.sort()
                return {
                    "len": len(scores),
                    "min": min(scores),
                    "max": max(scores),
                    "avg": sum(scores) / len(scores),
                }

    def get_user_groups(self):
        groups = {
            "following_followers": self.get_users(self.get_following_followers(), lookup=False),
            "following_only": self.get_users(self.get_following_only(), lookup=False),
            "followers_only": self.get_users(self.get_followers_only(), lookup=False),
            "others": self.get_users(self.get_others(), lookup=False),
        }
        return groups

    def get_statistics(self):
        uncached_user_ids = self.get_uncached_user_ids()
        users_with_scores = self.get_users_with_scores()
        users_without_scores = self.get_users_without_scores()

        statistics = {
            "number_of_uncached_users": len(uncached_user_ids),
            "number_of_cached_users": len(self._users),
            "number_of_cached_scored_users": len(users_with_scores),
            "number_of_cached_unscored_users": len(users_without_scores),
            "scores": self._get_user_score_statistics(users_with_scores),

        }

        for group_name, group_users in self.get_user_groups().items():
            statistics[group_name] = self._get_user_score_statistics(group_users)

        return statistics


if __name__ == '__main__':
    import identities

    logging.basicConfig(level=logging.INFO)

    identity = identities.AndrewTathamPi2Identity(None)

    logging.info(pprint.pformat(identity.users.get_statistics()))

    all_user_ids = identity.users.get_uncached_user_ids()[:20]

    identity.users.get_users(all_user_ids)

    logging.info(pprint.pformat(identity.users.get_statistics()))

    identity.users.score_users()

    logging.info(pprint.pformat(identity.users.get_statistics()))

    identity.users.get_leaderboard()
