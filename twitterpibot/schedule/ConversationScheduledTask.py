import random

from apscheduler.triggers.interval import IntervalTrigger


from twitterpibot.processing.Conversational import prompts_list_cold
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet



class ConversationScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=17, minutes=random.randint(0, 59))

    def on_run(self):
        text = "@" + self.identity.converse_with + " " + random.choice(prompts_list_cold)
        self.identity.twitter.send(OutgoingTweet(text=text))
