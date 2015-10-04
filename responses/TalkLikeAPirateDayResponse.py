from Response import Response
import random
import datetime
from TalkLikeAPirateDayScheduledTask import piracy
class TalkLikeAPirateDayResponse(Response):
    def Condition(args, inboxItem):
        today = datetime.date.today()
        isTalkLikeAPirateDay = bool(today.month == 9 and today.day == 19)
        return super(TalkLikeAPirateDayResponse, args).Condition(inboxItem) and isTalkLikeAPirateDay


    def Respond(args, inboxItem):
        response = random.choice(piracy) + " #TalkLikeAPirateDay" 
        args.ReplyWith(inboxItem, response)

        