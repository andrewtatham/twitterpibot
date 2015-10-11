
from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler
from PhotoScheduledTask import PhotoScheduledTask
import logging
from ExceptionHandler import Handle
from EdBallsDay import EdBallsDay
from Wikipedia import Wikipedia
from MonitorScheduledTask import MonitorScheduledTask
from TrendsScheduledTask import TrendsScheduledTask
from RateLimitsScheduledTask import RateLimitsScheduledTask
from SuggestedUsersScheduledTask import SuggestedUsersScheduledTask
from KatieHopkinsScheduledTask import KatieHopkinsScheduledTask
from UserListsScheduledTask import UserListsScheduledTask
from WeatherScheduledTask import WeatherScheduledTask
from BotBlockerScheduledTask import BotBlockerScheduledTask
from JokesScheduledTask import JokesScheduledTask
from TimelapseScheduledTask import TimelapseScheduledTask
from SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
from SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
from NightTimelapseScheduledTask import NightTimelapseScheduledTask
from SunTimelapseScheduledTask import SunTimelapseScheduledTask
from SavedSearchScheduledTask import SavedSearchScheduledTask
from TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from MidnightScheduledTask import MidnightScheduledTask
from SongScheduledTask import SongScheduledTask

global hardware




class Schedule(object):
    def __init__(self, *args, **kwargs):

        self._scheduler = BackgroundScheduler()
        self.jobs = [Wikipedia(),
            EdBallsDay(),
            TalkLikeAPirateDayScheduledTask(),
            MonitorScheduledTask(),
            TrendsScheduledTask(),
            SuggestedUsersScheduledTask(),
            #RateLimitsScheduledTask(),
            #KatieHopkinsScheduledTask(),
            UserListsScheduledTask(),
            WeatherScheduledTask(),
            JokesScheduledTask(), 
            #TimelapseScheduledTask(),
            SunriseTimelapseScheduledTask(),
            SunsetTimelapseScheduledTask(),
            NightTimelapseScheduledTask(),
            SunTimelapseScheduledTask(),
            SavedSearchScheduledTask(),
            MidnightScheduledTask(),
            SongScheduledTask()
            ]


        if hardware.iswindows:
            self.jobs.append(BotBlockerScheduledTask())

        if not hardware.iswindows:
            self.jobs.append(PhotoScheduledTask())

        for job in self.jobs:
            job.onInit()
            self._scheduler.add_job(self.RunWrapper, args=[job], trigger = job.GetTrigger())

        return super(Schedule, self).__init__(*args, **kwargs)

    def RunWrapper(args, task):
        try:   
            task.onRun()
        except Exception as e:
            Handle(e)

    def Start(args):
        args._scheduler.start()
    def Stop(args):
        args._scheduler.shutdown()
        for job in args.jobs:
            job.onStop()
        
    def add(args, job):
        job.onInit()
        args._scheduler.add_job(args.RunWrapper, args=[job], trigger = job.GetTrigger())
