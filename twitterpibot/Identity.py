import twitterpibot.hardware.hardware as hardware
from twitterpibot.schedule.StreamSavedTrendsScheduledTask import StreamSavedTrendsScheduledTask

is_andrewtathampi = hardware.isRaspberryPi or hardware.iswindows
is_andrewtathampi2 = hardware.isRaspberryPi2 and not is_andrewtathampi

screen_name = None
if is_andrewtathampi:
    screen_name = "andrewtathampi"
elif is_andrewtathampi2:
    screen_name = "andrewtathampi2"

print("Identity = " + screen_name)

import twitterpibot.twitter.TwitterHelper as TwitterHelper

id = TwitterHelper.init(screen_name)


def get_responses():
    from twitterpibot.responses.SongResponse import SongResponse
    from twitterpibot.responses.PhotoResponse import PhotoResponse
    from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
    from twitterpibot.responses.RetweetResponse import RetweetResponse
    from twitterpibot.responses.FatherTedResponse import FatherTedResponse
    from twitterpibot.responses.BotBlockerResponse import BotBlockerResponse
    from twitterpibot.responses.ThanksResponse import ThanksResponse
    from twitterpibot.responses.HelloResponse import HelloResponse
    from twitterpibot.responses.RestartResponse import RestartResponse
    from twitterpibot.responses.TimelapseResponse import TimelapseResponse
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

    if hardware.ispicamattached or hardware.iswebcamattached:
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
    # from twitterpibot.schedule.TimelapseScheduledTask import TimelapseScheduledTask
    from twitterpibot.schedule.SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
    from twitterpibot.schedule.SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
    from twitterpibot.schedule.NightTimelapseScheduledTask import NightTimelapseScheduledTask
    from twitterpibot.schedule.SunTimelapseScheduledTask import SunTimelapseScheduledTask
    from twitterpibot.schedule.SavedSearchScheduledTask import SavedSearchScheduledTask
    from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
    from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
    from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
    from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
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

    if is_andrewtathampi and (hardware.iswebcamattached or hardware.ispicamattached):
        scheduledjobs.extend([
            # TimelapseScheduledTask(),
            SunriseTimelapseScheduledTask(),
            SunsetTimelapseScheduledTask(),
            NightTimelapseScheduledTask(),
            SunTimelapseScheduledTask()
        ])
        if not hardware.iswindows:
            scheduledjobs.append(PhotoScheduledTask())
    if hardware.ispiglowattached or hardware.isunicornhatattached:
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
             StreamTweetsTask(TwitterHelper.GetStreamer())
             #StreamTweetsTask(TwitterHelper.GetStreamer(), topic="#Leeds")
    ]
    if hardware.ispiglowattached or hardware.isunicornhatattached:
        tasks.extend([
            LightsTask(),
            FadeTask()
        ])
    return tasks
