from twitterpibot.ExceptionHandler import Handle
import twitterpibot.Identity as Identity
from apscheduler.schedulers.background import BackgroundScheduler
import logging
logger = logging.getLogger(__name__)

def RunWrapper(task):
    try:
        task.onRun()
    except Exception as e:
        Handle(e)


def start():
    _scheduler.start()


def stop():
    _scheduler.shutdown()
    for job in _jobs:
        job.onStop()


def add(job):
    trigger = job.GetTrigger()
    logger.info("[MySchedule] adding " + str(type(job)) + " @ " + str(trigger))
    _scheduler.add_job(RunWrapper, args=[job], trigger=trigger)


_scheduler = BackgroundScheduler()
_jobs = Identity.get_scheduled_jobs()

for job in _jobs:
    add(job)
