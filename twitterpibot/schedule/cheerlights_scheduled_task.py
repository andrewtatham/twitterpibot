import random

from apscheduler.triggers.interval import IntervalTrigger

import identities_pis
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.logic import cheerlights


class CheerlightsScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(24, 48), minutes=random.randint(0, 59))

    def on_run(self):
        colour = random.choice(cheerlights.cheerlight_colours)
        if colour:
            text = random.choice(cheerlights.texts[colour])

            if text:
                text = "@cheerlights " + text
                self.identity.twitter.send(OutgoingTweet(text=text))


if __name__ == '__main__':
    identity = identities_pis.AndrewTathamPiIdentity(None)
    task = CheerlightsScheduledTask(identity)
    task.on_run()
