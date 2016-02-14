import datetime
import logging

logger = logging.getLogger(__name__)


class Lists(object):
    def __init__(self, identity, list_names):
        self._identity = identity
        self._list_names = list_names
        self._sets = {}
        self._list_ids = {}

    def update_lists(self):

        logger.info("Getting lists")
        twitter_lists = self._identity.twitter.show_owned_lists()
        twitter_lists_names_set = set(map(lambda tl: tl["name"], twitter_lists))
        any_new_lists_created = False
        for list_name in self._list_names:
            if list_name not in twitter_lists_names_set:
                logger.info("Creating list: " + list_name)
                self._identity.twitter.create_list(name=list_name, mode="private")
                any_new_lists_created = True

        if any_new_lists_created:
            logger.info("Getting lists again")
            twitter_lists = self._identity.twitter.show_owned_lists()

        for twitter_list in twitter_lists:
            list_id = twitter_list["id_str"]
            list_name = twitter_list["name"]
            logger.info("Getting List Members: " + list_name)
            members = self._identity.twitter.get_list_members(list_id=list_id)
            self._list_ids[list_name] = list_id
            self._sets[list_name] = set(map(lambda member: member["id_str"], members["users"]))

    def add_user(self, list_name, user_id, screen_name):
        if not self._sets or not self._list_ids:
            self.update_lists()

        list_id = self._list_ids[list_name]
        self._identity.twitter.add_user_to_list(list_id, user_id, screen_name)
        self._sets[list_name].add(user_id)

    def update_user(self, user):
        if not self._sets or not self._list_ids:
            self.update_lists()

        user.is_arsehole = "Arseholes" in self._sets and user.id in self._sets.get("Arseholes")
        user.is_reply_less = "Reply Less" in self._sets and user.id in self._sets.get("Reply Less")
        user.is_do_not_retweet = "Dont Retweet" in self._sets and user.id in self._sets.get("Dont Retweet")
        user.is_retweet_more = "Retweet More" in self._sets and user.id in self._sets.get("Retweet More")
        user.is_bot = "Awesome Bots" in self._sets and user.id in self._sets.get("Awesome Bots")
        user.is_friend = "Friends" in self._sets and user.id in self._sets.get("Friends")

        user.updated = datetime.datetime.utcnow()
