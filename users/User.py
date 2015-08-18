import logging
import datetime
class User(object):
    def __init__(self, id, *args, **kwargs):

        self.id = id
        self.updated = None

        self.isRetweetMore = False
        self.isBot = False        
        self.isFriend = False

        




    def isStale(args):

        if args.updated is None:
            return True

        delta = datetime.datetime.utcnow() - args.updated
        mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
        return mins > 45 



    def update(args, lists):
        
        for list in lists:
            if args.id in list.members:

                if list.name == "Retweet More":
                    self.isRetweetMore = True
                elif list.name == "Awesome Bots":
                    self.isBot = True                
                elif list.name == "Friends":
                    self.isFriend = True
                else:
                    logging.warn('Unknown list name: ' +  list.name)


        args.updated = datetime.datetime.utcnow()