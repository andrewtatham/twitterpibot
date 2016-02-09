import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.Identity import converse_with
from twitterpibot.processing.Conversational import prompts_list_cold
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.TwitterHelper import send


class ConversationScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=17)

    def on_run(self):
        text = "@" + converse_with + " " + random.choice(prompts_list_cold)
        send(OutgoingTweet(text=text))
