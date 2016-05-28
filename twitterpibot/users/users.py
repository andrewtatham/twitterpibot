import datetime
import logging
import random
from threading import Lock

from twitterpibot.users import lists
from twitterpibot.users.user import User

logger = logging.getLogger(__name__)


class Users(object):
    def __init__(self, identity):
        self._identity = identity
        self._users = {}

        self._following = set()
        self._followers = set()
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
        logger.info("getting {} users".format(len(user_ids)))
        users = []
        cached = list(filter(lambda u: u in self._users, user_ids))
        logger.info("{} cached users".format(len(cached)))
        to_lookup = None
        if lookup:
            to_lookup = list(filter(lambda u: not u in self._users, user_ids))
            logger.info("to lookup {} users".format(len(to_lookup)))

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

        logger.info("returning {} users".format(len(users)))
        return users

    def update_user(self, user):

        self._lists.update_user_list_memberships(user)

        user.follower = user.id_str in self._followers
        user.following = user.id_str in self._following

        user.update_flags()

        user.updated = datetime.datetime.utcnow()

    def friends(self, friends):
        logger.info("[%s] Friends %s" % (self._identity.screen_name, len(friends)))
        self._following = set([str(f) for f in friends])

    def get_following(self):
        if not self._following:
            self._following = self._identity.twitter.get_following()
            logger.info("[%s] following %s" % (self._identity.screen_name, len(self._following)))
        return self._following

    def get_followers(self):
        if not self._followers:
            self._followers = self._identity.twitter.get_followers()
            logger.info("[%s] followers %s" % (self._identity.screen_name, len(self._followers)))
        return self._followers

    def score_users(self, n=None):
        users_without_scores = list(filter(lambda u: not u.user_score, list(self._users.values())))
        random.shuffle(users_without_scores)
        logger.info("{} users without scores".format(len(users_without_scores)))
        if n:
            users_without_scores = users_without_scores[:n]
        logger.info("scoring {} users".format(len(users_without_scores)))
        for user in users_without_scores:
            user.get_user_score()

        users_with_scores = list(filter(lambda u: u.user_score, list(self._users.values())))
        logger.info("{} with scores".format(len(users_with_scores)))
        return len(users_with_scores)

    def get_leaderboard(self, n=3):
        users_with_scores = list(filter(lambda u: u.user_score, list(self._users.values())))
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
        self._identity.twitter.follow(user_id=user_id)
        self._following.add(user_id)

    def unfollow(self, user_id):
        logger.info("unfollowing user id %s" % user_id)
        self._identity.twitter.unfollow(user_id=user_id)
        self._forget_user_id(user_id)

    def block(self, user_id):
        logger.info("blocking user id %s" % user_id)
        self._identity.twitter.block(user_id=user_id)
        self._forget_user_id(user_id)

    def report(self, user_id):
        logger.info("reporting user id %s" % user_id)
        self._identity.twitter.report(user_id=user_id)
        self._forget_user_id(user_id)

    def _forget_user_id(self, user_id):
        if user_id in self._following:
            self._following.remove(user_id)
        if user_id in self._followers:
            self._followers.remove(user_id)
        if user_id in self._users:
            self._users.pop(user_id, None)

    def _get_unfollowed_list_members(self, list_names):
        to_follow = set()
        for list_name in list_names:
            if list_name in self._lists._sets:
                list_members = self._lists._sets[list_name]
                if list_members and self._following:
                    to_follow.update(list_members.difference(self._following))
        return to_follow

    def _get_subscribed_list_members(self):
        members = set()
        subscriptions = self._identity.twitter.get_list_subscriptions()
        for subscribed_list in subscriptions["lists"]:
            subscribed_list_members = self._identity.twitter.get_list_members(list_id=subscribed_list["id_str"])
            ids = set(map(lambda usr: usr["id_str"], subscribed_list_members["users"]))
            members.update(ids)
        return members

    def _get_followed_subscribed_list_members(self):
        followed = set()
        members = self._get_subscribed_list_members()
        if members and self._following:
            followed.update(members.intersection(self._following))
        return followed

    def _get_unfollowed_subscribed_list_members(self):
        unfollowed = set()
        members = self._get_subscribed_list_members()
        if members and self._following:
            unfollowed.update(members.difference(self._following))
        return unfollowed

    def _get_followed_inactive(self):
        inactive = set([id_str for id_str, user in self._users.items() if user.is_inactive()])
        return self._following.intersection(inactive)


if __name__ == '__main__':
    import identities

    identity = identities.AndrewTathamPi2Identity(None)

    all_user_ids = set()
    all_user_ids.update(identity.users.get_following())
    all_user_ids.update(identity.users.get_followers())
    all_user_ids = list(all_user_ids)
    print(len(all_user_ids))
    random.shuffle(all_user_ids)
    all_user_ids = all_user_ids[:20]

    identity.users.get_users(all_user_ids)

    try:
        no_of_scores = identity.users.score_users()
        print(no_of_scores)
    except Exception as ex:
        print(ex)
    finally:
        identity.users.get_leaderboard()
