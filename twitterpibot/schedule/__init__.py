import logging

from apscheduler.schedulers.background import BackgroundScheduler

from twitterpibot.exceptionmanager import handle
from twitterpibot.schedule.MonitorScheduledTask import GlobalMonitorScheduledTask

logger = logging.getLogger(__name__)


def _run_wrapper(task):
    try:
        task.on_run()
    except Exception as e:
        handle(task.identity, e)


def start():
    for job in _scheduled_jobs:
        add(job)
    _scheduler.start()


def stop():
    logger.info("Stopping")
    _scheduler.shutdown()
    for scheduled_job in _scheduled_jobs:
        scheduled_job.on_stop()
    logger.info("Stopped")


def add(scheduled_job):
    trigger = scheduled_job.get_trigger()
    logger.info("[MySchedule] adding " + str(type(scheduled_job)) + " @ " + str(trigger))
    _scheduler.add_job(_run_wrapper, args=[scheduled_job], trigger=trigger, name=str(scheduled_job))


_scheduler = BackgroundScheduler()
_scheduled_jobs = []


def set_scheduled_jobs(identities):
    global _scheduled_jobs
    _scheduled_jobs = [GlobalMonitorScheduledTask(None)]
    for identity in identities:
        _scheduled_jobs.extend(identity.get_scheduled_jobs())
