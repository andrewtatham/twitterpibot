from twitterpibot.responses.Response import Response

from twitterpibot.users.BotBlocker import BotBlocker


class BotBlockerResponse(Response):
    def __init__(self):
        self.blocker = BotBlocker()

    def condition(self, inbox_item):
        is_new_follower = inbox_item.is_event and not inbox_item.from_me and inbox_item.to_me and inbox_item.isFollow
        return is_new_follower

    def respond(self, inbox_item):
        if self.blocker.IsUserBot(inbox_item.source):
            self.blocker.BlockUser(inbox_item.source)
