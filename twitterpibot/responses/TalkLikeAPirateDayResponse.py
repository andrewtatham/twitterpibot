from twitterpibot.responses.Response import Response
import random
import datetime
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import piracy

from twitterpibot.twitter.TwitterHelper import reply_with


class TalkLikeAPirateDayResponse(Response):
    def Condition(self, inbox_item):
        today = datetime.date.today()
        isTalkLikeAPirateDay = bool(today.month == 9 and today.day == 19)
        return super(TalkLikeAPirateDayResponse, self).Condition(inbox_item) and isTalkLikeAPirateDay

    def Respond(self, inbox_item):
        response = random.choice(piracy) + " #TalkLikeAPirateDay"
        reply_with(inbox_item, response)
