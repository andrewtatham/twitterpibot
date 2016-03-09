import abc

import colorama

from twitterpibot import hardware
from twitterpibot.logic.internationalwomensday import InternationalWomensDayScheduledTask, \
    InternationalWomensDayResponse
from twitterpibot.identities.statistics import Statistics
from twitterpibot.responses.ConversationResponse import ConversationResponse
from twitterpibot.responses.EggPunResponse import EggPunResponse
from twitterpibot.responses.FatherTedResponse import FatherTedResponse
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.GifResponse import GifResponse
from twitterpibot.responses.HelloResponse import HelloResponse
from twitterpibot.responses.HiveMindResponse import HiveMindResponse
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
from twitterpibot.responses.PhotoResponse import PhotoResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.responses.SongResponse import SongResponse
from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
from twitterpibot.responses.ThanksResponse import ThanksResponse
from twitterpibot.responses.TimelapseResponse import TimelapseResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
from twitterpibot.schedule.BlankTweetScheduledTask import BlankTweetScheduledTask
from twitterpibot.schedule.ConversationScheduledTask import ConversationScheduledTask
from twitterpibot.schedule.EdBallsDay import EdBallsDay
from twitterpibot.schedule.EggPunScheduledTask import EggPunScheduledTask
from twitterpibot.schedule.FollowScheduledTask import FollowScheduledTask
from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
from twitterpibot.schedule.LightsScheduledTask import LightsScheduledTask
from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
from twitterpibot.schedule.MonitorScheduledTask import MonitorScheduledTask
from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
from twitterpibot.schedule.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask
from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
from twitterpibot.schedule.SubscribedListsScheduledTask import SubscribedListsScheduledTask
from twitterpibot.schedule.SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
from twitterpibot.schedule.SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask
from twitterpibot.schedule.ZenOfPythonScheduledTask import ZenOfPythonScheduledTask
from twitterpibot.tasks.FadeTask import FadeTask
from twitterpibot.tasks.LightsTask import LightsTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter.twitterhelper import TwitterHelper
from twitterpibot.users.lists import Lists
from twitterpibot.users.users import Users

all_identities = []


class Identity(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name
        self.admin_screen_name = "andrewtatham"
        self.converse_with = None
        self.tokens = None
        self.streamer = None
        self.users = Users(self)
        self.lists = Lists(self)
        self.twitter = TwitterHelper(self)
        self.following = set()
        self.colour = colorama.Fore.WHITE
        self.id_str = None
        self.profile_image_url = None  # todo init
        self.statistics = Statistics()

    @abc.abstractmethod
    def get_tasks(self):
        return []

    @abc.abstractmethod
    def get_scheduled_jobs(self):
        return []

    @abc.abstractmethod
    def get_responses(self):
        return []


class BotIdentity(Identity):
    def __init__(self, screen_name):
        super(BotIdentity, self).__init__(screen_name)

    def get_tasks(self):
        return [
            StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return [
            MonitorScheduledTask(self),
            MidnightScheduledTask(self),
            UserListsScheduledTask(self, andrewtatham),
            SubscribedListsScheduledTask(self, andrewtatham),
            FollowScheduledTask(self),
        ]

    def get_responses(self):
        return []


class AndrewTathamIdentity(Identity):
    def __init__(self, slave_identities):
        super(AndrewTathamIdentity, self).__init__("andrewtatham")
        self.admin_screen_name = "andrewtatham"
        self.slave_identities = slave_identities
        self.id_str = "19201332"

    def get_tasks(self):
        return [
            StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return [
        ]

    def get_responses(self):
        return [
            HiveMindResponse(self)
        ]


class AndrewTathamPiIdentity(BotIdentity):
    def __init__(self):
        super(AndrewTathamPiIdentity, self).__init__("andrewtathampi")
        self.admin_screen_name = "andrewtatham"
        self.converse_with = "andrewtathampi2"
        self.colour = colorama.Fore.MAGENTA
        self.id_str = "2935295111"

    def get_tasks(self):
        return get_bot_tasks(self)

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPiIdentity, self).get_scheduled_jobs()
        jobs.extend(get_bot_scheduled_jobs(self))
        return jobs

    def get_responses(self):
        return get_bot_responses(self)


class AndrewTathamPi2Identity(BotIdentity):
    def __init__(self):
        super(AndrewTathamPi2Identity, self).__init__("andrewtathampi2")
        self.admin_screen_name = "andrewtatham"
        self.converse_with = "andrewtathampi"
        self.colour = colorama.Fore.CYAN
        self.id_str = "3892161801"

    def get_tasks(self):
        return get_bot_tasks(self)

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPi2Identity, self).get_scheduled_jobs()
        jobs.extend(get_bot_scheduled_jobs(self))
        return jobs

    def get_responses(self):
        return get_bot_responses(self)


class NumberwangHostIdentity(BotIdentity):
    def __init__(self):
        super(NumberwangHostIdentity, self).__init__("numberwang_host")
        self.admin_screen_name = "andrewtatham"
        self.id_str = "4904547543"

    def get_tasks(self):
        return []

    def get_scheduled_jobs(self):
        contestants = [
            [julienumberwang, simonnumberwang],
            [julienumberwang, simonnumberwang],
            [julienumberwang, simonnumberwang],
            [andrewtatham, julienumberwang],
            [andrewtatham, simonnumberwang],
            [andrewtathampi, andrewtathampi2]
        ]
        jobs = super(NumberwangHostIdentity, self).get_scheduled_jobs()
        jobs.append(NumberwangHostScheduledTask(self, contestants))
        return jobs


class JulieNumberwangIdentity(BotIdentity):
    def __init__(self):
        super(JulieNumberwangIdentity, self).__init__("JulieNumberwang")
        self.admin_screen_name = "andrewtatham"
        self.id_str = "4912246174"

    def get_tasks(self):
        return []


class SimonNumberwangIdentity(BotIdentity):
    def __init__(self):
        super(SimonNumberwangIdentity, self).__init__("SimonNumberwang")
        self.admin_screen_name = "andrewtatham"
        self.id_str = "4912203173"

    def get_tasks(self):
        return []



class EggPunBotIdentity(BotIdentity):
    def __init__(self):
        super(EggPunBotIdentity, self).__init__("eggpunbot")
        self.id_str = "706393659244154880"

    def get_scheduled_jobs(self):
        jobs = super(EggPunBotIdentity, self).get_scheduled_jobs()
        jobs.append(EggPunScheduledTask(self))
        return jobs

    def get_responses(self):
        return [EggPunResponse(self)]


andrewtathampi = AndrewTathamPiIdentity()
andrewtathampi2 = AndrewTathamPi2Identity()
slaves = [andrewtathampi, andrewtathampi2]
andrewtatham = AndrewTathamIdentity(slaves)
numberwang_host = NumberwangHostIdentity()
julienumberwang = JulieNumberwangIdentity()
simonnumberwang = SimonNumberwangIdentity()
eggpunbot = EggPunBotIdentity()

if hardware.is_raspberry_pi_2:
    all_identities = [
        andrewtatham,
        andrewtathampi,
        andrewtathampi2,
        numberwang_host,
        julienumberwang,
        simonnumberwang,
        eggpunbot
    ]
else:
    all_identities = [
        andrewtatham,
        andrewtathampi,
        andrewtathampi2,
        numberwang_host,
        julienumberwang,
        simonnumberwang,
        eggpunbot,
    ]


def get_all_tasks():
    tasks = []
    for i in all_identities:
        t = i.get_tasks()
        tasks.extend(t)
    return tasks


def get_all_scheduled_jobs():
    scheduled_jobs = []
    for i in all_identities:
        scheduled_jobs.extend(i.get_scheduled_jobs())
    return scheduled_jobs





def get_bot_scheduled_jobs(identity):
    scheduledjobs = [
        WikipediaScheduledTask(identity),
        EdBallsDay(identity),
        TalkLikeAPirateDayScheduledTask(identity),
        WeatherScheduledTask(identity),
        JokesScheduledTask(identity),
        SongScheduledTask(identity),
        ConversationScheduledTask(identity),
        ZenOfPythonScheduledTask(identity),
        BlankTweetScheduledTask(identity),
        HappyBirthdayScheduledTask(identity),
        # EggPunScheduledTask(identity),
        InternationalWomensDayScheduledTask(identity),

    ]

    if hardware.is_linux and (hardware.is_webcam_attached or hardware.is_picam_attached):
        scheduledjobs.extend([
            PhotoScheduledTask(identity),
            SunriseTimelapseScheduledTask(identity),
            SunsetTimelapseScheduledTask(identity),
            RegularTimelapseScheduledTask(identity)
        ])
    if hardware.is_piglow_attached \
            or hardware.is_unicornhat_attached \
            or hardware.is_blinksticknano_attached:
        scheduledjobs.extend([
            LightsScheduledTask(identity)
        ])
    return scheduledjobs


def get_bot_responses(identity):
    responses = [
        SongResponse(identity),
        TalkLikeAPirateDayResponse(identity),
        ConversationResponse(identity),
        EggPunResponse(identity),
        ThanksResponse(identity),
        HelloResponse(identity),
        InternationalWomensDayResponse(identity),
        Magic8BallResponse(identity),
    ]
    if hardware.is_picam_attached or hardware.is_webcam_attached:
        responses.extend([
            PhotoResponse(identity),
            TimelapseResponse(identity)
        ])
    responses.extend([
        GifResponse(identity),
        FatherTedResponse(identity),
        FavoriteResponse(identity),
        RetweetResponse(identity),
    ])
    return responses


def get_bot_tasks(identity):
    tasks = [
        StreamTweetsTask(identity)
    ]
    if hardware.is_piglow_attached \
            or hardware.is_unicornhat_attached \
            or hardware.is_blinksticknano_attached:
        tasks.extend([
            LightsTask(),
            FadeTask()
        ])
    return tasks
