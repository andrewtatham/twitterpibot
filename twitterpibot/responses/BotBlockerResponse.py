from Response import Response
from twitterpibot.users.BotBlocker import BotBlocker


class BotBlockerResponse(Response):
    def __init__(self):
        self.blocker = BotBlocker()

    def Condition(self, inbox_item):
        isNewFollower = inbox_item.isEvent and not inbox_item.from_me and inbox_item.to_me and inbox_item.isFollow
        if isNewFollower:
            return self.blocker.IsUserBot(inbox_item.source)
        else:
            return False

    def Respond(self, inbox_item):
        self.blocker.BlockUser(inbox_item.source)
