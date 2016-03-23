import random

from twitterpibot.responses.Response import Response, mentioned_reply_condition
import twitterpibot.hardware


class PhotoResponse(Response):
    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item) \
               and "photo" in inbox_item.words

    def respond(self, inbox_item):
        photos = twitterpibot.hardware.take_photo("temp", "PhotoResponse", "jpg")
        if any(photos):
            messages = ["cheese!", "smile!"]
            self.identity.twitter.reply_with(
                inbox_item=inbox_item,
                text=random.choice(messages),
                as_tweet=True,
                file_paths=photos)
