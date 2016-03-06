import random
from threading import Timer

from twitterpibot.responses.Response import Response


class HiveMindResponse(Response):
    def __init__(self, master_identity):
        Response.__init__(self, master_identity)

    def condition(self, inbox_item):
        return inbox_item.is_event

    def respond(self, inbox_item):

        funcs = []
        if inbox_item.from_me:

            if inbox_item.is_favorite:
                for identity in self.identity.slave_identities:
                    funcs.append(lambda i=identity: i.twitter.create_favorite(status_id=inbox_item.targetObjectID))
            elif inbox_item.is_retweet:
                for identity in self.identity.slave_identities:
                    funcs.append(lambda i=identity: i.twitter.retweet(status_id=inbox_item.targetObjectID))
        if funcs:
            for f in funcs:
                if f:
                    t = Timer(random.randint(15, 45), f)
                    t.start()
