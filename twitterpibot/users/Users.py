import logging
from twitterpibot.users.User import User

logger = logging.getLogger(__name__)
class Users(object):
    def __init__(self, identity):
        self._identity = identity
        self._users = {}

    def get_user(self, user_id=None, user_data=None):
        if user_id and not user_data:
            logger.debug("looking up user %s"  % user_id)
            user_data = self._identity.twitter.lookup_user(user_id=user_id)[0]

        if user_data:
            user_id = user_data["id_str"]
            logger.debug(user_data)
            if user_id not in self._users:
                self._users[user_id] = User(user_data, self._identity.screen_name)

            if self._users[user_id].is_stale():
                self._identity.lists.update_user(user=self._users[user_id])

            return self._users[user_id]
