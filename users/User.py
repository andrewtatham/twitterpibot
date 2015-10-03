import logging
import datetime
import threading

class User(object):
    def __init__(self, data, *args, **kwargs):


        self.id = data["id_str"]

        self.isMe = bool(self.id == "2935295111")

        self.name = data["name"]
        self.screen_name = data["screen_name"]
        self.description = data["description"]

        self.verified = bool(data["verified"])
        self.location = data["location"]

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









    def isStale(args):
        with args.lock:
            if args.updated is None:
                return True

            delta = datetime.datetime.utcnow() - args.updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            return mins > 45 



    def update(args, lists):
        with args.lock:
            for list in lists.values():
                if list.ContainsUser(args.id):

                    if list.name == "Arseholes":
                        args.isArsehole = True # This is my favourite line in this code
                        print("Is member of " + list.name)

                    if list.name == "Reply Less":
                        args.isReplyLess = True
                        print("Is member of " + list.name)

                    if list.name == "Retweet More":
                        args.isRetweetMore = True
                        print("Is member of " + list.name)

                    if list.name == "Awesome Bots":
                        args.isBot = True                
                        print("Is member of " + list.name)
                  
                    if list.name == "Friends":
                        args.isFriend = True
                        print("Is member of " + list.name)

            args.updated = datetime.datetime.utcnow()