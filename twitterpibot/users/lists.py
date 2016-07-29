import logging

logger = logging.getLogger(__name__)
default_lists = [
    "Reply Less",
    "Arseholes",
    "Dont Retweet",
    "Retweet More",
    "Awesome Bots",
    "Friends",
    "Blocked Users",
    "Possibly Bots"
]


class Lists(object):
    def __init__(self, identity):
        self._identity = identity
        self._list_names = default_lists
        self._sets = {}
        self._list_ids = {}

    def update_lists(self):

        logger.info("[%s] Getting lists " % self._identity.screen_name)
        twitter_lists = self._identity.twitter.show_owned_lists()
        twitter_lists_names_set = set(map(lambda tl: tl["name"], twitter_lists))
        any_new_lists_created = False
        for list_name in self._list_names:
            if list_name not in twitter_lists_names_set:
                logger.info("[%s] Creating list: %s" % (self._identity.screen_name, list_name))
                self._identity.twitter.create_list(name=list_name, mode="private")
                any_new_lists_created = True

        if any_new_lists_created:
            logger.debug("[%s] Getting lists" % self._identity.screen_name)
            twitter_lists = self._identity.twitter.show_owned_lists()

        for twitter_list in twitter_lists:
            list_id = twitter_list["id_str"]
            list_name = twitter_list["name"]
            logger.debug("[%s] getting list members: %s" % (self._identity.screen_name, list_name))
            members = self._identity.twitter.get_list_members(list_id=list_id)
            self._list_ids[list_name] = list_id
            self._sets[list_name] = set(map(lambda member: member["id_str"], members["users"]))
            logger.debug("[%s] %s members: %s" % (self._identity.screen_name, list_name, str(self._sets[list_name])))

    def add_user_to_list(self, list_name, user_id, screen_name):
        if not self._sets or not self._list_ids:
            self.update_lists()

        logger.debug("{} adding user {} {} to list {}".format(
            self._identity.screen_name, user_id, screen_name, list_name))
        list_id = self._list_ids[list_name]
        self._identity.twitter.add_user_to_list(list_id, user_id, screen_name)
        self._sets[list_name].add(user_id)

    def update_user_list_memberships(self, user):
        if not self._sets or not self._list_ids:
            self.update_lists()

        list_memberships = set()
        for list_name in self._sets:
            if user.id_str in self._sets[list_name]:
                list_memberships.add(list_name)

        user.update_list_memberships(list_memberships)

    def get_list_members(self, list_name):
        if not self._sets or not self._list_ids:
            self.update_lists()

        return self._sets[list_name]
