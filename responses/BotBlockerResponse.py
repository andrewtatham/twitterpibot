
from Response import Response

from MyTwitter import MyTwitter
from BotBlocker import BotBlocker






class BotBlockerResponse(Response):
    def __init__(self, *args, **kwargs):
        self.blocker = BotBlocker()

    def Condition(args, inboxItem):
        isNewFollower = inboxItem.isEvent and not inboxItem.from_me and inboxItem.to_me and inboxItem.isFollow
        if isNewFollower:
            return args.blocker.IsUserBot(user_id = inboxItem.sourceID, username = inboxItem.followerName, screen_name =inboxItem.followerScreenName, description =inboxItem.followerDescription)
        else:
            return False


    def Respond(args, inboxItem):
        args.blocker.BlockUser(inboxItem.sourceID, inboxItem.followerScreenName)

        


