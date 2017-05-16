import colorama

from identity import BotIdentity
from twitterpibot.hardware import myhardware
from twitterpibot.schedule.ScrollNewsHeadlinesScheduledTask import ScrollNewsHeadlinesScheduledTask


class ScrollBotIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(ScrollBotIdentity, self).__init__(
            screen_name="scroll_bot",
            id_str="863364063316893696",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.YELLOW

    def get_scheduled_jobs(self):
        jobs = super().get_scheduled_jobs()
        if myhardware.is_scroll_bot and myhardware.is_scroll_hat_attached:
            jobs.append(ScrollNewsHeadlinesScheduledTask(self))
        return jobs
