import abc

from twitterpibot.hardware import hardware
# from twitterpibot.responses.BotBlockerResponse import BotBlockerResponse
from twitterpibot.responses.ConversationResponse import ConversationResponse
from twitterpibot.responses.FatherTedResponse import FatherTedResponse
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.HelloResponse import HelloResponse
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
from twitterpibot.responses.RestartResponse import RestartResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.responses.SongResponse import SongResponse
from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
from twitterpibot.responses.ThanksResponse import ThanksResponse
from twitterpibot.schedule.ConversationScheduledTask import ConversationScheduledTask
from twitterpibot.schedule.EdBallsDay import EdBallsDay
from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
from twitterpibot.schedule.LightsScheduledTask import LightsScheduledTask
from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
from twitterpibot.schedule.MonitorScheduledTask import MonitorScheduledTask
from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.ZenOfPythonScheduledTask import ZenOfPythonScheduledTask
from twitterpibot.tasks.FadeTask import FadeTask
from twitterpibot.tasks.LightsTask import LightsTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter import TwitterHelper
from twitterpibot.users.Lists import Lists
from twitterpibot.users.Users import Users


def get_scheduled_jobs(identity, is_andrewtathampi=False, is_andrewtathampi2=False):
    from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask
    scheduledjobs = [
        MonitorScheduledTask(identity),
        #  SuggestedUsersScheduledTask(identity),
        UserListsScheduledTask(identity),
        # SavedSearchScheduledTask(identity),
        MidnightScheduledTask(identity),
        # BotBlockerScheduledTask(identity),
        # TrendsScheduledTask(identity),
        WikipediaScheduledTask(identity),
        EdBallsDay(identity),
        TalkLikeAPirateDayScheduledTask(identity),
        WeatherScheduledTask(identity),
        JokesScheduledTask(identity),
        SongScheduledTask(identity),
        # HappyBirthdayScheduledTask(identity),
        ConversationScheduledTask(identity),
        ZenOfPythonScheduledTask(identity)
    ]

    # if is_andrewtathampi:
    #     pass
    # elif is_andrewtathampi2:
    #     scheduledjobs.extend([
    #         StreamTrendsScheduledTask()
    #     ])

    if hardware.is_linux and (hardware.is_webcam_attached or hardware.is_picam_attached):
        from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
        # from twitterpibot.schedule.TimelapseScheduledTask import TimelapseScheduledTask
        from twitterpibot.schedule.SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
        from twitterpibot.schedule.SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
        # from twitterpibot.schedule.SunTimelapseScheduledTask import SunTimelapseScheduledTask
        # from twitterpibot.schedule.NightTimelapseScheduledTask import NightTimelapseScheduledTask
        from twitterpibot.schedule.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask

        scheduledjobs.extend([
            PhotoScheduledTask(identity),
            # TimelapseScheduledTask(identity),
            SunriseTimelapseScheduledTask(identity),
            SunsetTimelapseScheduledTask(identity),
            # NightTimelapseScheduledTask(identity),
            # SunTimelapseScheduledTask(identity),
            RegularTimelapseScheduledTask(identity)
        ])
    if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
        scheduledjobs.extend([
            LightsScheduledTask(identity)
        ])
    return scheduledjobs


def get_responses(identity, is_andrewtathampi=False, is_andrewtathampi2=False):
    responses = [
        RestartResponse(identity),
        # BotBlockerResponse(identity),
        SongResponse(identity),
        TalkLikeAPirateDayResponse(identity),
        ConversationResponse(identity),
        ThanksResponse(identity),
        HelloResponse(identity),
        Magic8BallResponse(identity)
    ]

    if is_andrewtathampi:
        pass
    elif is_andrewtathampi2:
        pass

    if hardware.is_picam_attached or hardware.is_webcam_attached:
        from twitterpibot.responses.PhotoResponse import PhotoResponse
        from twitterpibot.responses.TimelapseResponse import TimelapseResponse
        responses.extend([
            PhotoResponse(identity),
            TimelapseResponse(identity)
        ])

    if is_andrewtathampi:
        pass
    elif is_andrewtathampi2:
        pass

    responses.extend([
        FatherTedResponse(identity),
        FavoriteResponse(identity),
        RetweetResponse(identity)
    ])

    return responses


class Identity(object):
    def __init__(self):
        self.admin_screen_name = None
        self.screen_name = None
        self.converse_with = None
        self.twitter = None
        self.tokens = None
        self.streamer = None
        self.users = Users(self)
        self.lists = Lists(self, list_names=[])

    @abc.abstractmethod
    def init(self):
        self.twitter = TwitterHelper.TwitterHelper(self)

    @abc.abstractmethod
    def get_tasks(self):
        return []

    @abc.abstractmethod
    def get_scheduled_jobs(self):
        return []

    @abc.abstractmethod
    def get_responses(self):
        return []


class andrewtatham(Identity):
    def init(self):
        self.admin_screen_name = "andrewtatham"
        self.screen_name = "andrewtatham"
        super(andrewtatham, self).init()

    def get_tasks(self):
        return [StreamTweetsTask(self)]

    def get_scheduled_jobs(self):
        return []

    def get_responses(self):
        return []


class andrewtathampi(Identity):
    def init(self):
        self.admin_screen_name = "andrewtatham"
        self.screen_name = "andrewtathampi"
        self.converse_with = "andrewtathampi2"
        self.lists = Lists(self, [
            "Reply Less",
            "Arseholes",
            "Dont Retweet",
            "Retweet More",
            "Awesome Bots",
            "Friends",
            "Blocked Users"
        ])

        super(andrewtathampi, self).init()

    def get_tasks(self):
        tasks = [StreamTweetsTask(self)]
        if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
            tasks.extend([
                LightsTask(),
                FadeTask()
            ])
        return tasks

    def get_scheduled_jobs(self):
        return get_scheduled_jobs(self, is_andrewtathampi=True)

    def get_responses(self):
        return get_responses(self, is_andrewtathampi=True)


class andrewtathampi2(Identity):
    def init(self):
        self.admin_screen_name = "andrewtatham"
        self.screen_name = "andrewtathampi2"
        self.converse_with = "andrewtathampi"
        self.lists = Lists(self, [
            "Reply Less",
            "Arseholes",
            "Dont Retweet",
            "Retweet More",
            "Awesome Bots",
            "Friends",
            "Blocked Users"
        ])
        super(andrewtathampi2, self).init()

    def get_tasks(self):
        tasks = [StreamTweetsTask(self)]
        if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
            tasks.extend([
                LightsTask(),
                FadeTask()
            ])
        return tasks

    def get_scheduled_jobs(self):
        return get_scheduled_jobs(self, is_andrewtathampi2=True)

    def get_responses(self):
        return get_responses(self, is_andrewtathampi2=True)


class numberwang_host(Identity):
    def init(self):
        self.admin_screen_name = "andrewtatham"
        self.screen_name = "numberwang_host"
        super(numberwang_host, self).init()

    def get_tasks(self):
        return [StreamTweetsTask(self)]

    def get_scheduled_jobs(self):
        return []

    def get_responses(self):
        return []
