from twitterpibot.processing import Conversational
from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class ConversationResponse(Response):
    def condition(self, inbox_item):
        return super(ConversationResponse, self).reply_condition(inbox_item) \
               and inbox_item.text_stripped in Conversational.prompts_and_responses

    def respond(self, inbox_item):
        response = Conversational.response(inbox_item.text_stripped)
        if response:
            reply_with(inbox_item, response)
