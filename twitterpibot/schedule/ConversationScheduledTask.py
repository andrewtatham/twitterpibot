import random
from twitterpibot import Identity
from twitterpibot.processing.Conversational import prompts_list
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


class ConversationScheduledTask(ScheduledTask):
    def onRun(self):
        text = "@" + Identity.converse_with + " " + random.choice(prompts_list)
        send(OutgoingTweet(text=text))
