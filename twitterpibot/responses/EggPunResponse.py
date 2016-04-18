from twitterpibot.logic import imagemanager, eggpuns, fsh
from twitterpibot.responses.Response import Response, mentioned_reply_condition, unmentioned_reply_condition


class EggPunResponse(Response):
    def condition(self, inbox_item):
        return (mentioned_reply_condition(inbox_item) or unmentioned_reply_condition(
            inbox_item)) and eggpuns.is_egg_pun_trigger(inbox_item.text_stripped)

    def respond(self, inbox_item):
        file_paths = None
        try:
            response = eggpuns.make_egg_pun_phrase(inbox_item.text, mask=inbox_item.text_stripped)
            if inbox_item.is_tweet:
                gif_text = eggpuns.get_gif_search_text()
                gif = imagemanager.get_gif(screen_name=self.identity.screen_name, text=gif_text)
                if gif:
                    file_paths = [gif]

            self.identity.twitter.quote_tweet(
                inbox_item=inbox_item,
                text=response,
                file_paths=file_paths)
        finally:
            fsh.delete_files(file_paths)
