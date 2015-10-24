from Response import Response
from twitterpibot.users.BotBlocker import BotBlocker


class BotBlockerResponse(Response):
    def __init__(self):
        self.blocker = BotBlocker()

    def Condition(self, inboxItem):
        isNewFollower = inboxItem.isEvent and not inboxItem.from_me and inboxItem.to_me and inboxItem.isFollow
        if isNewFollower:
            return self.blocker.IsUserBot(inboxItem.source)
        else:
            return False

    def Respond(self, inboxItem):
        self.blocker.BlockUser(inboxItem.source)
