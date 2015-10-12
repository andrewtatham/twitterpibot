
from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
import random
from TwitterHelper import Send

piracy = [
    "You can always trust the untrustworthy because you can always trust that they will be untrustworthy. Its the trustworthy you can't trust.",
    "If ye can't trust a pirate, ye damn well can't trust a merchant either!",
    "Yarrrr! there be ony two ranks of leader amongst us pirates! Captain and if your really notorious then it's Cap'n!",
    "Not all treasure is silver and gold",
    "There comes a time in most men's lives where they feel the need to raise the Black Flag",
    "The rougher the seas, the smoother we sail. Ahoy!",
    "Drink up me hearties yo-ho-ho! a pirates life for me"
] 
class TalkLikeAPirateDayScheduledTask(ScheduledTask):
        
    def GetTrigger(args):
        return CronTrigger(month = 9, day = 19, minute = "*/10")
 
    def onRun(args):
        text = random.choice(piracy) + " #TalkLikeAPirateDay"
        tweet = OutgoingTweet(text=text)
        Send(tweet)