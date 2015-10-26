import twitterpibot.hardware.hardware as hardware
from twitterpibot.schedule.StreamSavedTrendsScheduledTask import StreamSavedTrendsScheduledTask
import twitterpibot.twitter.TwitterHelper as TwitterHelper

import logging
logger = logging.getLogger(__name__)

is_andrewtathampi = hardware.is_raspberry_pi or hardware.is_windows or hardware.is_mac_osx
is_andrewtathampi2 = hardware.is_raspberry_pi_2 and not is_andrewtathampi

screen_name = None
if is_andrewtathampi:
    screen_name = "andrewtathampi"
elif is_andrewtathampi2:
    screen_name = "andrewtathampi2"

logger.info("Identity: " + screen_name)

twid = None
def init():
    global twid
    twid = TwitterHelper.init(screen_name)


def get_responses():
    from twitterpibot.responses.SongResponse import SongResponse
    from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
    from twitterpibot.responses.RetweetResponse import RetweetResponse
    from twitterpibot.responses.FatherTedResponse import FatherTedResponse
    from twitterpibot.responses.BotBlockerResponse import BotBlockerResponse
    from twitterpibot.responses.ThanksResponse import ThanksResponse
    from twitterpibot.responses.HelloResponse import HelloResponse
    from twitterpibot.responses.RestartResponse import RestartResponse
    from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse

    responses = [
        RestartResponse(),
        #BotBlockerResponse()
    ]

    if is_andrewtathampi:
        responses.extend([
            SongResponse(),
            TalkLikeAPirateDayResponse(),
            ThanksResponse(),
            HelloResponse(),
            Magic8BallResponse()
        ])
    elif is_andrewtathampi2:
        pass

    if hardware.is_picam_attached or hardware.is_webcam_attached:
        from twitterpibot.responses.PhotoResponse import PhotoResponse
        from twitterpibot.responses.TimelapseResponse import TimelapseResponse
        responses.extend([
            PhotoResponse(),
            TimelapseResponse()
        ])

    if is_andrewtathampi:
        responses.extend([
            FatherTedResponse(),
            RetweetResponse()
        ])
    elif is_andrewtathampi2:
        pass

    return responses


def get_scheduled_jobs():
    from twitterpibot.schedule.EdBallsDay import EdBallsDay
    from twitterpibot.schedule.Wikipedia import Wikipedia
    from twitterpibot.schedule.MonitorScheduledTask import MonitorScheduledTask
    from twitterpibot.schedule.TrendsScheduledTask import TrendsScheduledTask
    from twitterpibot.schedule.SuggestedUsersScheduledTask import SuggestedUsersScheduledTask
    from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
    from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
    from twitterpibot.schedule.BotBlockerScheduledTask import BotBlockerScheduledTask
    from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
    from twitterpibot.schedule.SavedSearchScheduledTask import SavedSearchScheduledTask
    from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
    from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
    from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
    from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
    from twitterpibot.schedule.LightsScheduledTask import LightsScheduledTask

    scheduledjobs = [
        MonitorScheduledTask(),
        SuggestedUsersScheduledTask(),
        UserListsScheduledTask(),
        SavedSearchScheduledTask(),
        MidnightScheduledTask(),
        #BotBlockerScheduledTask(),
        StreamSavedTrendsScheduledTask()
    ]

    if is_andrewtathampi:
        scheduledjobs.extend([
            TrendsScheduledTask(),
            Wikipedia(),
            EdBallsDay(),
            TalkLikeAPirateDayScheduledTask(),
            WeatherScheduledTask(),
            JokesScheduledTask(),
            SongScheduledTask(),
            HappyBirthdayScheduledTask()
        ])
    elif is_andrewtathampi2:
        pass

    if is_andrewtathampi and (hardware.is_webcam_attached or hardware.is_picam_attached):
        from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
        # from twitterpibot.schedule.TimelapseScheduledTask import TimelapseScheduledTask
        from twitterpibot.schedule.SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
        from twitterpibot.schedule.SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
        from twitterpibot.schedule.NightTimelapseScheduledTask import NightTimelapseScheduledTask
        from twitterpibot.schedule.SunTimelapseScheduledTask import SunTimelapseScheduledTask
        scheduledjobs.extend([
            PhotoScheduledTask(),
            # TimelapseScheduledTask(),
            SunriseTimelapseScheduledTask(),
            SunsetTimelapseScheduledTask(),
            NightTimelapseScheduledTask(),
            SunTimelapseScheduledTask()
        ])
    if hardware.is_linux and (hardware.is_piglow_attached or hardware.is_unicornhat_attached):
        scheduledjobs.extend([
            LightsScheduledTask()
        ])
    return scheduledjobs


def get_tasks():
    from twitterpibot.tasks.ProcessInboxTask import ProcessInboxTask
    from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
    from twitterpibot.tasks.FadeTask import FadeTask
    from twitterpibot.tasks.LightsTask import LightsTask
    tasks = [ProcessInboxTask(),
             StreamTweetsTask(TwitterHelper.GetStreamer()),
             StreamTweetsTask(TwitterHelper.GetStreamer(),topic="#Leeds")
    ]
    if hardware.is_linux and (hardware.ispiglowattached or hardware.isunicornhatattached):
        tasks.extend([
            LightsTask(),
            FadeTask()
        ])
    return tasks
