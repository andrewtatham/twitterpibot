import abc
import datetime
import os

import colorama

import twitterpibot
from twitterpibot import hardware
from twitterpibot.logic.conversational import ConversationScheduledTask
from twitterpibot.logic.whenisinternationalmensday import WhenIsIMDScheduledTask, \
    WhenIsInternationalMensDayResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
from twitterpibot.responses.EggPunResponse import EggPunResponse
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.ReplyResponse import ReplyResponse
from twitterpibot.responses.HelloResponse import HelloResponse
from twitterpibot.responses.HiveMindResponse import HiveMindResponse
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
from twitterpibot.responses.PhotoResponse import PhotoResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.responses.SongResponse import SongResponse
from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
from twitterpibot.responses.ThanksResponse import ThanksResponse
from twitterpibot.responses.TimelapseResponse import TimelapseResponse
from twitterpibot.responses.x_or_y_response import X_Or_Y_Response
from twitterpibot.schedule.BlankTweetScheduledTask import BlankTweetScheduledTask
from twitterpibot.logic.ed_balls_day import TweetEdBallsDayScheduledTask, StreamEdBallsDayScheduledTask
from twitterpibot.schedule.EggPunScheduledTask import EggPunScheduledTask
from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
from twitterpibot.schedule.LightsScheduledTask import LightsScheduledTask
from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
from twitterpibot.schedule.RegularTimelapseScheduledTask import RegularTimelapseScheduledTask
from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
from twitterpibot.schedule.SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
from twitterpibot.schedule.SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask
from twitterpibot.schedule.ZenOfPythonScheduledTask import ZenOfPythonScheduledTask
from twitterpibot.tasks.FadeTask import FadeTask
from twitterpibot.tasks.LightsTask import LightsTask
from twitterpibot.schedule.FollowScheduledTask import FollowScheduledTask
from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
from twitterpibot.schedule.MonitorScheduledTask import IdentityMonitorScheduledTask
from twitterpibot.schedule.SubscribedListsScheduledTask import SubscribedListsScheduledTask
from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter import twitterhelper
from twitterpibot.users import lists, users


class Statistics(object):
    def __init__(self):
        self._stats = {}

    def reset(self):
        self._stats = {}

    def increment(self, key):
        if key not in self._stats:
            self._stats[key] = 0
        self._stats[key] += 1

    def get_statistics(self):
        text = "Stats at " + datetime.datetime.now().strftime("%x %X") + os.linesep
        for key, val in self._stats.items():
            text += str(val) + " " + key + os.linesep
        return text

    def record_incoming_tweet(self, tweet):
        self.increment("Incoming Tweets")

    def record_incoming_direct_message(self, dm):
        self.increment("Incoming Direct Messages")

    def record_incoming_event(self, event):
        self.increment("Incoming Event")

    def record_connection(self):
        self.increment("Connnections")

    def record_outgoing_tweet(self):
        self.increment("Outgoing Tweets")

    def record_outgoing_direct_message(self):
        self.increment("Outgoing Direct Messages")

    def record_outgoing_song_lyric(self):
        self.increment("Outgoing Song Lyrics")

    def record_warning(self):
        self.increment("Warnings")

    def record_error(self):
        self.increment("Errors")

    def record_retweet(self):
        self.increment("Retweets")

    def record_favourite(self):
        self.increment("Favourites")


class Identity(object):
    def __init__(self, screen_name, id_str, ):
        self.screen_name = screen_name
        self.id_str = id_str
        self.admin_screen_name = "andrewtatham"
        self.converse_with = None
        self.tokens = None
        self.streamer = None
        self.users = users.Users(self)
        self.lists = lists.Lists(self)
        self.twitter = twitterhelper.TwitterHelper(self)
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
        return [
            TweetEdBallsDayScheduledTask(self),
        ]

    @abc.abstractmethod
    def get_responses(self):
        return []


class BotIdentity(Identity):
    def __init__(self, screen_name, id_str, admin_identity):
        super(BotIdentity, self).__init__(screen_name, id_str)
        self.admin_identity = admin_identity

    def get_tasks(self):
        return [
            StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        jobs = super(BotIdentity, self).get_scheduled_jobs()
        jobs.extend([
            IdentityMonitorScheduledTask(self),
            MidnightScheduledTask(self),
            UserListsScheduledTask(self, self.admin_identity),
            SubscribedListsScheduledTask(self, self.admin_identity),
            FollowScheduledTask(self),

        ])
        return jobs

    def get_responses(self):
        return []


def get_pi_scheduled_jobs(identity, converse_with_identity):



    scheduledjobs = [
        WikipediaScheduledTask(identity),
        TalkLikeAPirateDayScheduledTask(identity),
        WeatherScheduledTask(identity),
        JokesScheduledTask(identity),
        SongScheduledTask(identity),
        ConversationScheduledTask(identity,converse_with_identity),
        ZenOfPythonScheduledTask(identity),
        BlankTweetScheduledTask(identity),
        HappyBirthdayScheduledTask(identity),
        # LocationScheduledTask(identity),
        # RaiseExceptionScheduledTask(identity),
        StreamEdBallsDayScheduledTask(identity, )

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


def get_pi_responses(identity):
    responses = [
        SongResponse(identity),
        TalkLikeAPirateDayResponse(identity),
        # LocationResponse(identity),
        X_Or_Y_Response(identity),
        EggPunResponse(identity),
        ThanksResponse(identity),
        HelloResponse(identity),
        Magic8BallResponse(identity),
    ]
    if hardware.is_picam_attached or hardware.is_webcam_attached:
        responses.extend([
            PhotoResponse(identity),
            TimelapseResponse(identity)
        ])
    responses.extend([
        ReplyResponse(identity),
        FavoriteResponse(identity),
        RetweetResponse(identity),
    ])
    return responses


def get_pi_tasks(identity):
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


class AndrewTathamIdentity(Identity):
    def __init__(self):
        super(AndrewTathamIdentity, self).__init__(
            screen_name="andrewtatham",
            id_str="19201332")

    def get_tasks(self):
        return [StreamTweetsTask(self)]

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamIdentity, self).get_scheduled_jobs()
        return jobs

    def get_responses(self):
        followers = [
            andrewtathampi,
            andrewtathampi2
        ]
        return [HiveMindResponse(self, followers)]


class AndrewTathamPiIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(AndrewTathamPiIdentity, self).__init__(
            screen_name="andrewtathampi",
            id_str="2935295111",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.MAGENTA

    def get_tasks(self):
        return get_pi_tasks(self)

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPiIdentity, self).get_scheduled_jobs()
        jobs.extend(get_pi_scheduled_jobs(self, andrewtathampi2))
        return jobs

    def get_responses(self):
        return get_pi_responses(self)


class AndrewTathamPi2Identity(BotIdentity):
    def __init__(self, admin_identity):
        super(AndrewTathamPi2Identity, self).__init__(
            screen_name="andrewtathampi2",
            id_str="3892161801",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.CYAN

    def get_tasks(self):
        return get_pi_tasks(self)

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPi2Identity, self).get_scheduled_jobs()
        jobs.extend(get_pi_scheduled_jobs(self, andrewtathampi))
        return jobs

    def get_responses(self):
        return get_pi_responses(self)


class NumberwangHostIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(NumberwangHostIdentity, self).__init__(
            screen_name="numberwang_host",
            id_str="4904547543",
            admin_identity=admin_identity)

    def get_tasks(self):
        return []

    def get_scheduled_jobs(self):
        contestants = [
            [julienumberwang, simonnumberwang],
            [julienumberwang, simonnumberwang],
            [julienumberwang, simonnumberwang],
            [andrewtatham, julienumberwang],
            [andrewtatham, simonnumberwang],
            [andrewtatham, andrewtathampi],
            [andrewtatham, andrewtathampi2],
            [andrewtathampi, andrewtathampi2]
        ]
        jobs = super(NumberwangHostIdentity, self).get_scheduled_jobs()
        jobs.append(NumberwangHostScheduledTask(self, contestants))
        return jobs


class JulieNumberwangIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(JulieNumberwangIdentity, self).__init__(
            screen_name="JulieNumberwang",
            id_str="4912246174",
            admin_identity=admin_identity)

    def get_tasks(self):
        return []


class SimonNumberwangIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(SimonNumberwangIdentity, self).__init__(
            screen_name="SimonNumberwang",
            id_str="4912203173",
            admin_identity=admin_identity)

    def get_tasks(self):
        return []


class EggPunBotIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(EggPunBotIdentity, self).__init__(
            screen_name="eggpunbot",
            id_str="706393659244154880",
            admin_identity=admin_identity)

    def get_scheduled_jobs(self):
        jobs = super(EggPunBotIdentity, self).get_scheduled_jobs()
        jobs.append(EggPunScheduledTask(self))
        return jobs

    def get_responses(self):
        return [EggPunResponse(self)]


class WhenIsInternationalMensDayBotIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(WhenIsInternationalMensDayBotIdentity, self).__init__(
            screen_name="WhenMensDay",
            id_str="708233017639215104",
            admin_identity=admin_identity)

    def get_scheduled_jobs(self):
        jobs = super(WhenIsInternationalMensDayBotIdentity, self).get_scheduled_jobs()
        jobs.append(WhenIsIMDScheduledTask(self))
        return jobs

    def get_responses(self):
        return [WhenIsInternationalMensDayResponse(self)]


if __name__ == "__main__":
    import twitterpibot.bootstrap

    andrewtatham = AndrewTathamIdentity()
    andrewtathampi = AndrewTathamPiIdentity(andrewtatham)
    andrewtathampi2 = AndrewTathamPi2Identity(andrewtatham)
    numberwang_host = NumberwangHostIdentity(andrewtatham)
    julienumberwang = JulieNumberwangIdentity(andrewtatham)
    simonnumberwang = SimonNumberwangIdentity(andrewtatham)
    eggpunbot = EggPunBotIdentity(andrewtatham)
    whenmensday = WhenIsInternationalMensDayBotIdentity(andrewtatham)

    if twitterpibot.hardware.is_raspberry_pi_2:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            numberwang_host,
            julienumberwang,
            simonnumberwang,
            eggpunbot,
            whenmensday
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
            whenmensday
        ]

    twitterpibot.bootstrap.run(all_identities)
