from twitterpibot.twitter import Lists
from twitterpibot.users.User import User
from twitterpibot.twitter.MyTwitter import MyTwitter

_users = {}


def get_user(user_id=None, user_data=None):
    if user_id and not user_data:
        with MyTwitter() as twitter:
            user_data = twitter.lookup_user(user_id=user_id)[0]

    if user_data:
        user_id = user_data["id_str"]

        if user_id not in _users:
            _users[user_id] = User(user_data)

        if _users[user_id].isStale():
            Lists.update_user(user=_users[user_id])

        return _users[user_id]
