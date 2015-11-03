from twitterpibot import MyUI
from twitterpibot.responses.Response import Response
from twitterpibot.twitter import TwitterHelper


class RestartResponse(Response):
    def Condition(self, inbox_item):
        return inbox_item.isDirectMessage and not inbox_item.from_me and inbox_item.to_me \
               and inbox_item.sender.screen_name == "andrewtatham" \
               and "restart" in inbox_item.words  # and not hardware.iswindows

    def Respond(self, inbox_item):
        MyUI.close()
        # if not hardware.iswindows:
        #    Send(OutgoingDirectMessage(
        #        text="Restarting...." + str(datetime.datetime.now())))

