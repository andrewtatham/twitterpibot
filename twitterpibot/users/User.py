import datetime
import threading
from twitterpibot.Identity import id


class User(object):
    def __init__(self, data):

        self.id = data["id_str"]

        self.isMe = bool(self.id == id)

        self.name = data["name"]
        self.screen_name = data["screen_name"]
        self.description = data["description"]

        self.verified = bool(data["verified"])
        self.location = data["location"]
        self.protected = bool(data["protected"])

        self.friends_count = int(data["friends_count"])
        self.followers_count = int(data["followers_count"])
        self.statuses_count = int(data["statuses_count"])

        self.updated = None

        self.isArsehole = False
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

    def update(self, lists):
        with self.lock:
            for list in lists.values():
                if list.ContainsUser(self.id):

                    if list.name == "Arseholes":
                        self.isArsehole = True  # This is my favourite line in this code
                        print("Is member of " + list.name)

                    if list.name == "Reply Less":
                        self.isReplyLess = True
                        print("Is member of " + list.name)

                    if list.name == "Retweet More":
                        self.isRetweetMore = True
                        print("Is member of " + list.name)

                    if list.name == "Awesome Bots":
                        self.isBot = True
                        print("Is member of " + list.name)

                    if list.name == "Friends":
                        self.isFriend = True
                        print("Is member of " + list.name)

            self.updated = datetime.datetime.utcnow()
