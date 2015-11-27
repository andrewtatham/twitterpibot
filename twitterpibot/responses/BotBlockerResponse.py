from twitterpibot.incoming.InboxItem import InboxItem
from twitterpibot.responses.Response import Response

from twitterpibot.users.BotBlocker import BotBlocker


class BotBlockerResponse(Response):
    def __init__(self):
        self.blocker = BotBlocker()

    def condition(self, inbox_item):
        is_new_follower = inbox_item.is_event and not inbox_item.from_me and inbox_item.to_me and inbox_item.isFollow
        if is_new_follower:
            return self.blocker.IsUserBot(inbox_item.source)
        else:
            return False

    def respond(self, inbox_item):
        self.blocker.BlockUser(inbox_item.source)
