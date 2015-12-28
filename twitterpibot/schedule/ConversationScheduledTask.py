import random
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot import Identity
from twitterpibot.processing.Conversational import prompts_list_cold
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


class ConversationScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(hours=2)

    def onRun(self):
        text = "@" + Identity.converse_with + " " + random.choice(prompts_list_cold)
        send(OutgoingTweet(text=text))
