from twitterpibot import MyUI
from twitterpibot.Identity import admin_screen_name
from twitterpibot.responses.Response import Response


class RestartResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and not inbox_item.from_me and inbox_item.to_me \
               and inbox_item.sender.screen_name == admin_screen_name \
               and inbox_item.words and "restart" in inbox_item.words

    def respond(self, inbox_item):
        MyUI.close()
