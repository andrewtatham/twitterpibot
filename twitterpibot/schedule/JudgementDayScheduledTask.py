import random
from apscheduler.triggers.interval import IntervalTrigger
from twitterpibot.logic import judgement_day, morse_code, leetspeak
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

__author__ = 'andrewtatham'


class JudgementDayScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(JudgementDayScheduledTask, self).__init__(identity)
        self._morse_code = morse_code.MorseCode()
        self._leetspeak = leetspeak.LeetSpeak()

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        morse = self._morse_code.encode(self._leetspeak.encode(judgement_day.phrase()))
        text = ".@" + self.identity.converse_with.screen_name + " " + morse
        self.identity.twitter.send(OutgoingTweet(text=text))
