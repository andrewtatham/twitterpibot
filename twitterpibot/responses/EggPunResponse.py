from twitterpibot.logic import GiphyWrapper
from twitterpibot.logic import eggpuns
from twitterpibot.responses.Response import Response


class EggPunResponse(Response):
    def condition(self, inbox_item):
        return super(EggPunResponse, self).reply_condition(inbox_item) \
               and "egg" in inbox_item.text

    def respond(self, inbox_item):
        response = eggpuns.get_egg_pun()
        file_paths = None
        if inbox_item.is_tweet:
            file_paths = [GiphyWrapper.get_gif("egg")]
        self.identity.twitter.reply_with(
            inbox_item=inbox_item,
            text=response,
            file_paths=file_paths)
