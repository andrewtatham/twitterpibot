from apscheduler.triggers.cron import CronTrigger
from colorama import Style, Fore
import psutil
import logging

from twitterpibot.hardware import myhardware
from twitterpibot.schedule.ScheduledTask import ScheduledTask

__author__ = 'andrewtatham'

logger = logging.getLogger(__name__)


class GlobalMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/20')

    def on_run(self):
        cpu = str(psutil.cpu_percent())
        mem = str(psutil.virtual_memory().percent)
        disk_space = myhardware.get_remaining_disk_space()

        text = 'cpu = ' + cpu + ' memory = ' + mem
        if disk_space:
            text += " disk = {}".format(disk_space)
        logger.info(Style.BRIGHT + Fore.BLUE + text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    task = GlobalMonitorScheduledTask(None)
    task.on_run()
