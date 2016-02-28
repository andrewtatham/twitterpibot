import logging

from apscheduler.schedulers.background import BackgroundScheduler

import twitterpibot.schedule.ConversationScheduledTask
import twitterpibot.schedule.EdBallsDay
import twitterpibot.schedule.JokesScheduledTask
import twitterpibot.schedule.LightsScheduledTask
import twitterpibot.schedule.MidnightScheduledTask
import twitterpibot.schedule.MonitorScheduledTask
import twitterpibot.schedule.SongScheduledTask
import twitterpibot.schedule.TalkLikeAPirateDayScheduledTask
import twitterpibot.schedule.UserListsScheduledTask
import twitterpibot.schedule.WeatherScheduledTask
import twitterpibot.schedule.ZenOfPythonScheduledTask
import twitterpibot.schedule.BlankTweetScheduledTask
import twitterpibot.schedule.WikipediaScheduledTask
import twitterpibot.schedule.PhotoScheduledTask
import twitterpibot.schedule.SunriseTimelapseScheduledTask
import twitterpibot.schedule.SunsetTimelapseScheduledTask
import twitterpibot.schedule.RegularTimelapseScheduledTask
import twitterpibot.schedule.FollowScheduledTask
from twitterpibot.ExceptionHandler import handle

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


def set_scheduled_jobs(scheduled_jobs):
    global _scheduled_jobs
    _scheduled_jobs = scheduled_jobs
