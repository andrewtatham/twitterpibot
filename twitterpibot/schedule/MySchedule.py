from twitterpibot.ExceptionHandler import handle
import twitterpibot.Identity as Identity
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)


def RunWrapper(task):
    try:
        task.onRun()
    except Exception as e:
        handle(e)


def start():
    _scheduler.start()


def stop():
    _scheduler.shutdown()
    for scheduled_job in _scheduled_jobs:
        scheduled_job.onStop()


def add(scheduled_job):
    trigger = scheduled_job.GetTrigger()
    logger.info("[MySchedule] adding " + str(type(scheduled_job)) + " @ " + str(trigger))
    _scheduler.add_job(RunWrapper, args=[scheduled_job], trigger=trigger)


_scheduler = BackgroundScheduler()
_scheduled_jobs = Identity.get_scheduled_jobs()

for job in _scheduled_jobs:
    add(job)
