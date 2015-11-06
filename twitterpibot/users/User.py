import datetime
import threading
from twitterpibot import Identity


class User(object):
    def __init__(self, data):

        self.id = data["id_str"]
        self.name = data["name"]
        self.screen_name = data["screen_name"]
        self.description = data["description"]

        self.isMe = bool(self.screen_name == Identity.screen_name)

        self.verified = bool(data["verified"])
        self.location = data["location"]
        self.protected = bool(data["protected"])

        self.friends_count = int(data["friends_count"])
        self.followers_count = int(data["followers_count"])
        self.statuses_count = int(data["statuses_count"])

        self.updated = None

        self.isArsehole = False
        self.is_do_not_retweet = False
        self.isRetweetMore = False
        self.isBot = False
        self.isFriend = False
        self.isReplyLess = False

        self.lock = threading.Lock()

    def isStale(self):
        with self.lock:
            if self.updated:
                delta = datetime.datetime.utcnow() - self.updated
                mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
                return mins > 45
            else:
                return True
