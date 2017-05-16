from apscheduler.triggers.cron import CronTrigger

from twitterpibot.hardware import myhardware, myperipherals
from twitterpibot.logic import feedhelper
from twitterpibot.schedule.ScheduledTask import ScheduledTask


def get_headlines():
    headlines = []
    headlines.extend()


class ScrollNewsHeadlinesScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ScrollNewsHeadlinesScheduledTask, self).__init__(identity)
        self._headlines = []

    def get_trigger(self):
        return CronTrigger(minute="*/15")

    def on_run(self):
        if myhardware.is_scroll_bot and myhardware.is_scroll_hat_attached:
            if not any(self._headlines):
                self._headlines = feedhelper.get_bbc_science_and_technology()

            if any(self._headlines):
                headline = self._headlines.pop()
                if headline:
                    myperipherals.myscrollhat.enqueue(headline)


if __name__ == '__main__':
    import identities_scrollbot

    identity = identities_scrollbot.ScrollBotIdentity()
    task = ScrollNewsHeadlinesScheduledTask(identity)
    task.on_run()
