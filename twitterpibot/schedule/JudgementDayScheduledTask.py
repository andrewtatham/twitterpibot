import random
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.logic import morse_code, leetspeak
from twitterpibot.logic.judgement_day import phrase
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

__author__ = 'andrewtatham'


class JudgementDayScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(JudgementDayScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        morse = morse_code.encode(leetspeak.encode(phrase()))
        text = ".@" + self.identity.converse_with.screen_name + " " + morse
        self.identity.twitter.send(OutgoingTweet(text=text))