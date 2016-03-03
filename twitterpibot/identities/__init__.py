import abc
import random

import colorama

import twitterpibot
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
from twitterpibot.twitter.TwitterHelper import TwitterHelper
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
        twitterpibot.schedule.MonitorScheduledTask.MonitorScheduledTask(identity),
        twitterpibot.schedule.MidnightScheduledTask.MidnightScheduledTask(identity),
        twitterpibot.schedule.WikipediaScheduledTask.WikipediaScheduledTask(identity),
        twitterpibot.schedule.EdBallsDay.EdBallsDay(identity),
        twitterpibot.schedule.TalkLikeAPirateDayScheduledTask.TalkLikeAPirateDayScheduledTask(identity),
        twitterpibot.schedule.WeatherScheduledTask.WeatherScheduledTask(identity),
        twitterpibot.schedule.JokesScheduledTask.JokesScheduledTask(identity),
        twitterpibot.schedule.SongScheduledTask.SongScheduledTask(identity),
        twitterpibot.schedule.ConversationScheduledTask.ConversationScheduledTask(identity),
        twitterpibot.schedule.ZenOfPythonScheduledTask.ZenOfPythonScheduledTask(identity),
        twitterpibot.schedule.BlankTweetScheduledTask.BlankTweetScheduledTask(identity),
        twitterpibot.schedule.FollowScheduledTask.FollowScheduledTask(identity)

    ]

    if twitterpibot.hardware.is_linux \
            and (twitterpibot.hardware.is_webcam_attached or twitterpibot.hardware.is_picam_attached):
        scheduledjobs.extend([
            twitterpibot.schedule.PhotoScheduledTask.PhotoScheduledTask(identity),
            twitterpibot.schedule.SunriseTimelapseScheduledTask.SunriseTimelapseScheduledTask(identity),
            twitterpibot.schedule.SunsetTimelapseScheduledTask.SunsetTimelapseScheduledTask(identity),
            twitterpibot.schedule.RegularTimelapseScheduledTask.RegularTimelapseScheduledTask(identity)
        ])
    if twitterpibot.hardware.is_piglow_attached \
            or twitterpibot.hardware.is_unicornhat_attached \
            or twitterpibot.hardware.is_blinksticknano_attached:
        scheduledjobs.extend([
            twitterpibot.schedule.LightsScheduledTask.LightsScheduledTask(identity)
        ])
    return scheduledjobs


def get_bot_responses(identity, is_andrewtathampi=False, is_andrewtathampi2=False):
    responses = [

        twitterpibot.responses.SongResponse.SongResponse(identity),
        twitterpibot.responses.TalkLikeAPirateDayResponse.TalkLikeAPirateDayResponse(identity),
        twitterpibot.responses.ConversationResponse.ConversationResponse(identity),
        twitterpibot.responses.ThanksResponse.ThanksResponse(identity),
        twitterpibot.responses.HelloResponse.HelloResponse(identity),
        twitterpibot.responses.Magic8BallResponse.Magic8BallResponse(identity)
    ]
    if twitterpibot.hardware.is_picam_attached or twitterpibot.hardware.is_webcam_attached:
        responses.extend([
            twitterpibot.responses.PhotoResponse.PhotoResponse(identity),
            twitterpibot.responses.TimelapseResponse.TimelapseResponse(identity)
        ])
    responses.extend([
        twitterpibot.responses.FatherTedResponse.FatherTedResponse(identity),
        twitterpibot.responses.FavoriteResponse.FavoriteResponse(identity),
        twitterpibot.responses.RetweetResponse.RetweetResponse(identity)
    ])
    return responses


def get_bot_tasks(identity):
    tasks = [
        twitterpibot.tasks.StreamTweetsTask.StreamTweetsTask(identity)
    ]
    if twitterpibot.hardware.is_piglow_attached \
            or twitterpibot.hardware.is_unicornhat_attached \
            or twitterpibot.hardware.is_blinksticknano_attached:
        tasks.extend([
            twitterpibot.tasks.LightsTask.LightsTask(),
            twitterpibot.tasks.FadeTask.FadeTask()
        ])
    return tasks


class Identity(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name
        self.admin_screen_name = None
        self.converse_with = None
        self.tokens = None
        self.streamer = None
        self.users = Users(self)
        self.lists = Lists(self, list_names=[])
        self.twitter = TwitterHelper(self)
        self.following = set()
        self.colour = colorama.Fore.WHITE
        self.id_str = None
        self.profile_image_url = None  # todo init

    @abc.abstractmethod
    def get_tasks(self):
        return []

    @abc.abstractmethod
    def get_scheduled_jobs(self):
        return []

    @abc.abstractmethod
    def get_responses(self):
        return []


class AndrewTathamIdentity(Identity):
    def __init__(self, slave_identities):
        Identity.__init__(self, "andrewtatham")
        self.admin_screen_name = "andrewtatham"
        self.lists = Lists(self, default_lists)
        self.slave_identities = slave_identities
        self.id_str = "19201332"

    def get_tasks(self):
        return [
            twitterpibot.tasks.StreamTweetsTask.StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return [
            twitterpibot.schedule.UserListsScheduledTask.UserListsScheduledTask(self, default_lists),
            twitterpibot.schedule.SubscribedListsScheduledTask.SubscribedListsScheduledTask(self)
        ]

    def get_responses(self):
        return [
            twitterpibot.responses.HiveMindResponse.HiveMindResponse(self)
        ]


class AndrewTathamPiIdentity(Identity):
    def __init__(self):
        Identity.__init__(self, "andrewtathampi")
        self.admin_screen_name = "andrewtatham"
        self.converse_with = "andrewtathampi2"
        self.lists = Lists(self, default_lists)
        self.colour = colorama.Fore.MAGENTA
        self.id_str = "2935295111"

    def get_tasks(self):
        return get_bot_tasks(self)

    def get_scheduled_jobs(self):
        return get_bot_scheduled_jobs(self, is_andrewtathampi=True)

    def get_responses(self):
        return get_bot_responses(self, is_andrewtathampi=True)


class AndrewTathamPi2Identity(Identity):
    def __init__(self):
        Identity.__init__(self, "andrewtathampi2")
        self.admin_screen_name = "andrewtatham"
        self.converse_with = "andrewtathampi"
        self.lists = Lists(self, default_lists)
        self.colour = colorama.Fore.CYAN
        self.id_str = "3892161801"

    def get_tasks(self):
        return get_bot_tasks(self)

    def get_scheduled_jobs(self):
        return get_bot_scheduled_jobs(self, is_andrewtathampi2=True)

    def get_responses(self):
        return get_bot_responses(self, is_andrewtathampi2=True)


class NumberwangHostIdentity(Identity):
    def __init__(self):
        Identity.__init__(self, "numberwang_host")
        self.admin_screen_name = "andrewtatham"
        self.id_str = "4904547543"

    def get_tasks(self):
        return [
            twitterpibot.tasks.StreamTweetsTask.StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return [NumberwangHostScheduledTask(self)]

    def get_responses(self):
        return []


class JulieNumberwangIdentity(Identity):
    def __init__(self):
        Identity.__init__(self, "JulieNumberwang")
        self.admin_screen_name = "andrewtatham"
        self.id_str = "4912246174"

    def get_tasks(self):
        return [
            twitterpibot.tasks.StreamTweetsTask.StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return []

    def get_responses(self):
        return []


class SimonNumberwangIdentity(Identity):
    def __init__(self):
        Identity.__init__(self, "SimonNumberwang")
        self.admin_screen_name = "andrewtatham"
        self.id_str = "4912203173"

    def get_tasks(self):
        return [
            twitterpibot.tasks.StreamTweetsTask.StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return []

    def get_responses(self):
        return []


all_identities = []
if not all_identities:
    andrewtathampi = AndrewTathamPiIdentity()
    andrewtathampi2 = AndrewTathamPi2Identity()
    slaves = [andrewtathampi, andrewtathampi2]
    andrewtatham = AndrewTathamIdentity(slaves)
    numberwang_host = NumberwangHostIdentity()
    julienumberwang = JulieNumberwangIdentity()
    simonnumberwang = SimonNumberwangIdentity()

    if twitterpibot.hardware.is_raspberry_pi_2:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            numberwang_host,
            julienumberwang,
            simonnumberwang
        ]
    else:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            # numberwang_host,
            # julienumberwang,
            # simonnumberwang
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


def get_numberwang_contestants():
    return random.choice([
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [andrewtatham, twitterpibot.identities.julienumberwang],
        [andrewtatham, twitterpibot.identities.simonnumberwang],
        [andrewtathampi, twitterpibot.identities.andrewtathampi2]
    ])
