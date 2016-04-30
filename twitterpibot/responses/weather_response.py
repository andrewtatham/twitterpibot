import logging

from twitterpibot.logic import bbc_weather_bot, weather
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.responses.Response import Response, unmentioned_reply_condition, mentioned_reply_condition

logger = logging.getLogger(__name__)

weather_screen_names = [
    bbc_weather_bot.screen_name,
    # "metoffice",
    # "bbcweather",
    # "BBCWthrWatchers"

]


class WeatherResponse(Response):
    def condition(self, inbox_item):
        return (
                   unmentioned_reply_condition(inbox_item, one_in=4) or
                   mentioned_reply_condition(inbox_item)
                   # todo  or is part of tracked conversation
               ) and (
                   inbox_item.sender and inbox_item.sender.screen_name in weather_screen_names
                   or weather.is_weather(inbox_item.text)
               )

    def respond(self, inbox_item):
        if inbox_item.sender.screen_name == bbc_weather_bot.screen_name:

            text, new_phrases = bbc_weather_bot.get_bbc_weather_bot_text(inbox_item.text)
            if text:
                text = ".@" + self.identity.converse_with + " " + text
                self.identity.twitter.quote_tweet(inbox_item=inbox_item, text=text)

            if new_phrases:
                self.identity.twitter.send(OutgoingDirectMessage(text=str(new_phrases)))

        elif inbox_item.sender.screen_name == self.identity.converse_with.screen_name:

            response = weather.get_weather_response(inbox_item.text)
            self.identity.twitter.reply_with(inbox_item=inbox_item, text=response)
        else:
            pass
