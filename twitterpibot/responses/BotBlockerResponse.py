from twitterpibot.responses.Response import Response

import twitterpibot.users.BotBlocker as BotBlocker


class BotBlockerResponse(Response):
    def condition(self, inbox_item):
        is_new_follower = inbox_item.is_event and not inbox_item.from_me and inbox_item.to_me and inbox_item.isFollow
        return is_new_follower

    def respond(self, inbox_item):
        BotBlocker.check_user(self.identity, inbox_item.source)
