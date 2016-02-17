import abc

import twitterpibot.hardware.hardware as hardware
# from twitterpibot.responses.BotBlockerResponse import BotBlockerResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
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
import twitterpibot.schedule.UserListsScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.ZenOfPythonScheduledTask import ZenOfPythonScheduledTask
from twitterpibot.schedule.BlankTweetScheduledTask import BlankTweetScheduledTask
from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask
from twitterpibot.tasks.FadeTask import FadeTask
from twitterpibot.tasks.LightsTask import LightsTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter import TwitterHelper
from twitterpibot.users.Lists import Lists
from twitterpibot.users.Users import Users

default_lists = [
    "Reply Less",
    "Arseholes",
    "Dont Retweet",
    "Retweet More",
    "Awesome Bots",
    "Friends",
    "Blocked Users"
]


def get_bot_scheduled_jobs(identity, is_andrewtathampi=False, is_andrewtathampi2=False):
    scheduledjobs = [
        MonitorScheduledTask(identity),
        #  SuggestedUsersScheduledTask(identity),

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
        ZenOfPythonScheduledTask(identity),
        BlankTweetScheduledTask(identity)
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


def get_bot_responses(identity, is_andrewtathampi=False, is_andrewtathampi2=False):
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
    def __init__(self, screen_name):
        self.screen_name = screen_name
        self.admin_screen_name = None
        self.converse_with = None
        self.twitter = None
        self.tokens = None
        self.streamer = None
        self.users = Users(self)
        self.lists = Lists(self, list_names=[])
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
    def __init__(self):
        super(andrewtatham, self).__init__("andrewtatham")
        self.admin_screen_name = "andrewtatham"
        self.lists = Lists(self, default_lists)

    def get_tasks(self):
        return [StreamTweetsTask(self)]

    def get_scheduled_jobs(self):
        identities = [
            ids["andrewtatham"],
            ids["andrewtathampi"],
            ids["andrewtathampi2"]
        ]
        return [
            twitterpibot.schedule.UserListsScheduledTask.UserListsScheduledTask(identities, default_lists)
        ]

    def get_responses(self):
        return []


class andrewtathampi(Identity):
    def __init__(self):
        super(andrewtathampi, self).__init__("andrewtathampi")
        self.admin_screen_name = "andrewtatham"
        self.converse_with = "andrewtathampi2"
        self.lists = Lists(self, default_lists)

    def get_tasks(self):
        tasks = [StreamTweetsTask(self)]
        if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
            tasks.extend([
                LightsTask(),
                FadeTask()
            ])
        return tasks

    def get_scheduled_jobs(self):
        return get_bot_scheduled_jobs(self, is_andrewtathampi=True)

    def get_responses(self):
        return get_bot_responses(self, is_andrewtathampi=True)


class andrewtathampi2(Identity):
    def __init__(self):
        super(andrewtathampi2, self).__init__("andrewtathampi2")
        self.admin_screen_name = "andrewtatham"
        self.converse_with = "andrewtathampi"
        self.lists = Lists(self, default_lists)

    def get_tasks(self):
        tasks = [StreamTweetsTask(self)]
        if hardware.is_piglow_attached or hardware.is_unicornhat_attached or hardware.is_blinksticknano_attached:
            tasks.extend([
                LightsTask(),
                FadeTask()
            ])
        return tasks

    def get_scheduled_jobs(self):
        return get_bot_scheduled_jobs(self, is_andrewtathampi2=True)

    def get_responses(self):
        return get_bot_responses(self, is_andrewtathampi2=True)


class numberwang_host(Identity):
    def __init__(self):
        super(numberwang_host, self).__init__("numberwang_host")
        self.admin_screen_name = "andrewtatham"

    def get_tasks(self):
        return []

    def get_scheduled_jobs(self):
        return [NumberwangHostScheduledTask(self)]

    def get_responses(self):
        return []


class JulieNumberwang(Identity):
    def __init__(self):
        super(JulieNumberwang, self).__init__("JulieNumberwang")
        self.admin_screen_name = "andrewtatham"

    def get_tasks(self):
        return []

    def get_scheduled_jobs(self):
        return []

    def get_responses(self):
        return []


class SimonNumberwang(Identity):
    def __init__(self):
        super(SimonNumberwang, self).__init__("SimonNumberwang")
        self.admin_screen_name = "andrewtatham"

    def get_tasks(self):
        return []

    def get_scheduled_jobs(self):
        return []

    def get_responses(self):
        return []


ids = {}
if hardware.is_raspberry_pi:
    ids["andrewtathampi"] = andrewtathampi(),
elif hardware.is_raspberry_pi_2:

    ids["andrewtatham"] = andrewtatham()
    ids["andrewtathampi"] = andrewtathampi()
    ids["andrewtathampi2"] = andrewtathampi2()
    ids["numberwang_host"] = numberwang_host()
    ids["JulieNumberwang"] = JulieNumberwang()
    ids["SimonNumberwang"] = SimonNumberwang()

else:
    ids["andrewtatham"] = andrewtatham()
    ids["andrewtathampi"] = andrewtathampi()
    ids["andrewtathampi2"] = andrewtathampi2()
    ids["numberwang_host"] = numberwang_host()
    ids["JulieNumberwang"] = JulieNumberwang()
    ids["SimonNumberwang"] = SimonNumberwang()


def get_all_tasks():
    tasks = []
    for key, identity in ids.items():
        tasks.extend(identity.get_tasks())
    return tasks


def get_all_scheduled_jobs():
    scheduled_jobs = []
    for key, identity in ids.items():
        scheduled_jobs.extend(identity.get_scheduled_jobs())
    return scheduled_jobs
