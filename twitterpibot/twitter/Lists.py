import datetime
import threading
from twitterpibot.twitter import TwitterHelper
from twitterpibot.twitter.MyTwitter import MyTwitter

__author__ = 'andrewtatham'

_lock = threading.Lock()
_sets = {}
_list_ids = {}
_lists = [
    "Reply Less",
    "Arseholes",
    "Dont Retweet",
    "Retweet More",
    "Awesome Bots",
    "Friends",
    "Bad Bots"

]


def update_lists():
    with _lock:
        with MyTwitter() as twitter:

            twitter_lists = twitter.show_owned_lists()["lists"]

            twitter_lists_set = set(map(lambda tl: tl["name"], twitter_lists))
            for list in _lists:
                if list not in twitter_lists_set:
                    twitter.create_list(name=list, mode="private")

            for twitter_list in twitter_lists:
                list_id = twitter_list["id_str"]
                list_name = twitter_list["name"]
                members = twitter.get_list_members(list_id=list_id)
                _list_ids[list_name] = list_id
                _sets[list_name] = set(map(lambda member: member["id_str"], members["users"]))


def add_user(list_name, user_id, screen_name):
    if not _sets or not _list_ids:
        update_lists()
    with _lock:
        list_id = _list_ids[list_name]
        TwitterHelper.add_user_to_list(list_id, user_id, screen_name)
        _sets[list_name].add(user_id)


def update_user(user):
    if not _sets or not _list_ids:
        update_lists()
    with _lock:
        user.is_arsehole = user.id in _sets["Arseholes"]
        user.is_reply_less = user.id in _sets["Reply Less"]
        user.is_do_not_retweet = user.id in _sets["Dont Retweet"]
        user.is_retweet_more = user.id in _sets["Retweet More"]
        user.is_bot = user.id in _sets["Awesome Bots"]
        user.is_friend = user.id in _sets["Friends"]

        user.updated = datetime.datetime.utcnow()
