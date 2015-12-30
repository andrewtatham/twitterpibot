from twitterpibot.ExceptionHandler import handle
import twitterpibot.Identity as Identity
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)


def _run_wrapper(task):
    try:
        task.onRun()
    except Exception as e:
        handle(e)


def start():
    _scheduler.start()


def stop():
    logger.info("Stopping")
    _scheduler.shutdown(wait=False)
    for scheduled_job in _scheduled_jobs:
        scheduled_job.onStop()
    logger.info("Stopped")


def add(scheduled_job):
    trigger = scheduled_job.GetTrigger()
    logger.info("[MySchedule] adding " + str(type(scheduled_job)) + " @ " + str(trigger))
    _scheduler.add_job(_run_wrapper, args=[scheduled_job], trigger=trigger, name=str(scheduled_job))


_scheduler = BackgroundScheduler()
_scheduled_jobs = Identity.get_scheduled_jobs()

for job in _scheduled_jobs:
    add(job)
