from Response import Response
import random
import datetime
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import piracy

from twitterpibot.twitter.TwitterHelper import ReplyWith


class TalkLikeAPirateDayResponse(Response):
    def Condition(self, inboxItem):
        today = datetime.date.today()
        isTalkLikeAPirateDay = bool(today.month == 9 and today.day == 19)
        return super(TalkLikeAPirateDayResponse, self).Condition(inboxItem) and isTalkLikeAPirateDay

    def Respond(self, inboxItem):
        response = random.choice(piracy) + " #TalkLikeAPirateDay"
        ReplyWith(inboxItem, response)
