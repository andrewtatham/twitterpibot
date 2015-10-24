from twitterpibot import MyUI
from twitterpibot.responses.Response import Response


class RestartResponse(Response):
    def Condition(self, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
               and inboxItem.sender.screen_name == "andrewtatham" \
               and "restart" in inboxItem.words  # and not hardware.iswindows

    def Respond(self, inboxItem):
        MyUI.Close()
