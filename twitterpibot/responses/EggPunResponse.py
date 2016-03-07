import random
from twitterpibot.logic import giphyhelper
from twitterpibot.logic import eggpuns
from twitterpibot.responses.Response import Response


class EggPunResponse(Response):
    def condition(self, inbox_item):
        return super(EggPunResponse, self).reply_condition(inbox_item) \
               and eggpuns.is_egg_pun_trigger(inbox_item.text)

    def respond(self, inbox_item):
        response = eggpuns.make_egg_pun_phrase(inbox_item.text)
        file_paths = None
        if inbox_item.is_tweet:
            gif_text = eggpuns.get_gif_search_text()
            file_paths = [giphyhelper.get_gif(screen_name=self.identity.screen_name, text=gif_text)]
        self.identity.twitter.reply_with(
            inbox_item=inbox_item,
            text=response,
            file_paths=file_paths)
