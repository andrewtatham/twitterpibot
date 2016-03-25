from twitterpibot.logic import imagemanager, replies
from twitterpibot.responses.Response import Response, mentioned_reply_condition


class ReplyResponse(Response):
    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item)

    def respond(self, inbox_item):
        response = replies.get_reply()
        file_paths = None
        if inbox_item.is_tweet:
            image = imagemanager.get_reply_image(screen_name=self.identity.screen_name, text=inbox_item.text_stripped)
            if image:
                file_paths = [image]
        self.identity.twitter.reply_with(
            inbox_item=inbox_item,
            text=response,
            file_paths=file_paths)
