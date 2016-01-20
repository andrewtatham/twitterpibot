import logging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.twitter.TwitterHelper as TwitterHelper

logger = logging.getLogger(__name__)

is_andrewtathampi = hardware.is_raspberry_pi or hardware.is_windows or hardware.is_mac_osx
is_andrewtathampi2 = not is_andrewtathampi and hardware.is_raspberry_pi_2

screen_name = None
converse_with = None
if is_andrewtathampi:
    screen_name = "andrewtathampi"
    converse_with = "andrewtathampi2"
elif is_andrewtathampi2:
    screen_name = "andrewtathampi2"
    converse_with = "andrewtathampi"

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
    from twitterpibot.responses.ThanksResponse import ThanksResponse
    from twitterpibot.responses.HelloResponse import HelloResponse
    from twitterpibot.responses.RestartResponse import RestartResponse
    from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
    from twitterpibot.responses.BotBlockerResponse import BotBlockerResponse
    from twitterpibot.responses.ConversationResponse import ConversationResponse
    from twitterpibot.responses.FavoriteResponse import FavoriteResponse

    responses = [
        RestartResponse(),
        BotBlockerResponse(),
        SongResponse(),
        TalkLikeAPirateDayResponse(),
        ConversationResponse(),
        ThanksResponse(),
        HelloResponse(),
        Magic8BallResponse()
    ]

    if is_andrewtathampi:
        pass
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
        pass
    elif is_andrewtathampi2:
        pass

    responses.extend([
        FatherTedResponse(),
        FavoriteResponse(),
        RetweetResponse()
    ])

    return responses


def get_scheduled_jobs():
    from twitterpibot.schedule.EdBallsDay import EdBallsDay
    from twitterpibot.schedule.Wikipedia import Wikipedia
    from twitterpibot.schedule.MonitorScheduledTask import MonitorScheduledTask
    from twitterpibot.schedule.TrendsScheduledTask import TrendsScheduledTask
    # from twitterpibot.schedule.SuggestedUsersScheduledTask import SuggestedUsersScheduledTask
    from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
    from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
    from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
    from twitterpibot.schedule.SavedSearchScheduledTask import SavedSearchScheduledTask
    from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
    from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
    from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
    # from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
    from twitterpibot.schedule.LightsScheduledTask import LightsScheduledTask
    from twitterpibot.schedule.StreamTrendsScheduledTask import StreamTrendsScheduledTask
    from twitterpibot.schedule.BotBlockerScheduledTask import BotBlockerScheduledTask
    from twitterpibot.schedule.ConversationScheduledTask import ConversationScheduledTask

    scheduledjobs = [
        MonitorScheduledTask(),
        #  SuggestedUsersScheduledTask(),
        UserListsScheduledTask(),
        SavedSearchScheduledTask(),
        MidnightScheduledTask(),
        BotBlockerScheduledTask(),
        TrendsScheduledTask(),
        Wikipedia(),
        EdBallsDay(),
        TalkLikeAPirateDayScheduledTask(),
        WeatherScheduledTask(),
        JokesScheduledTask(),
        SongScheduledTask(),
        # HappyBirthdayScheduledTask(),
        ConversationScheduledTask()
    ]

    if is_andrewtathampi:
        pass
    elif is_andrewtathampi2:
        scheduledjobs.extend([
            StreamTrendsScheduledTask()
        ])

    if hardware.is_linux and (hardware.is_webcam_attached or hardware.is_picam_attached):
        from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
        # from twitterpibot.schedule.TimelapseScheduledTask import TimelapseScheduledTask
        from twitterpibot.schedule.SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
        from twitterpibot.schedule.SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
        # from twitterpibot.schedule.SunTimelapseScheduledTask import SunTimelapseScheduledTask
        # from twitterpibot.schedule.NightTimelapseScheduledTask import NightTimelapseScheduledTask
        from twitterpibot.schedule.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask

        scheduledjobs.extend([
            PhotoScheduledTask(),
            # TimelapseScheduledTask(),
            SunriseTimelapseScheduledTask(),
            SunsetTimelapseScheduledTask(),
            # NightTimelapseScheduledTask(),
            # SunTimelapseScheduledTask(),
            RegularTimelapseScheduledTask()
        ])
    if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
        scheduledjobs.extend([
            LightsScheduledTask()
        ])
    return scheduledjobs


def get_tasks():
    from twitterpibot.tasks.ProcessInboxTask import ProcessInboxTask
    from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
    from twitterpibot.tasks.FadeTask import FadeTask
    from twitterpibot.tasks.LightsTask import LightsTask
    tasks = [
        ProcessInboxTask(),
        StreamTweetsTask(TwitterHelper.get_streamer()),
        StreamTweetsTask(TwitterHelper.get_streamer(
            topic="magic eight ball,#MagicEightBall,magic 8 ball,#Magic8Ball", topic_name="#Magic8Ball"), core=True)
    ]
    if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
        tasks.extend([
            LightsTask(),
            FadeTask()
        ])
    return tasks
