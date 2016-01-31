import random
import datetime

from twitterpibot.responses.Response import Response
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import piracy
from twitterpibot.twitter.TwitterHelper import reply_with


class TalkLikeAPirateDayResponse(Response):
    def condition(self, inbox_item):
        today = datetime.date.today()
        is_talk_like_a_pirate_day = bool(today.month == 9 and today.day == 19)
        return is_talk_like_a_pirate_day and super(TalkLikeAPirateDayResponse, self).reply_condition(inbox_item)

    def respond(self, inbox_item):
        response = random.choice(piracy) + " #TalkLikeAPirateDay"
        reply_with(inbox_item, response)
