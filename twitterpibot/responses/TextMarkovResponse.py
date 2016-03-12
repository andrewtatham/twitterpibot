from twitterpibot.responses.MarkovResponse import MarkovResponse
from twitterpibot.text import textfilehelper


class TextMarkovResponse(MarkovResponse):
    def __init__(self, identity, text_name):
        super(TextMarkovResponse, self).__init__(identity, textfilehelper.get_text(text_name))

    def condition(self, inbox_item):
        return super(TextMarkovResponse, self).mentioned_reply_condition(inbox_item=inbox_item)

    def respond(self, inbox_item):
        super(TextMarkovResponse, self).respond(inbox_item=inbox_item)
