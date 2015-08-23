import logging
import datetime
from multiprocessing import Lock
class User(object):
    def __init__(self, id, *args, **kwargs):

        self.id = id
        self.updated = None

        self.isRetweetMore = False
        self.isBot = False        
        self.isFriend = False
        self.lock = Lock()

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

                    if list.name == "Retweet More":
                        args.isRetweetMore = True
                        print("Is member of " + list.name)

                    elif list.name == "Awesome Bots":
                        args.isBot = True                
                        print("Is member of " + list.name)
                  
                    elif list.name == "Friends":
                        args.isFriend = True
                        print("Is member of " + list.name)
                    
                    else:
                        
                        logging.warn('Unknown list name: ' +  list.name)

            args.updated = datetime.datetime.utcnow()