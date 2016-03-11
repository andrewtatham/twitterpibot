import colorama

import twitterpibot
from twitterpibot import hardware
from twitterpibot.identities import Identity, BotIdentity
from twitterpibot.logic.whenisinternationalmensday import WhenIsInternationalMensDayScheduledTask, \
    WhenIsInternationalMensDayResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
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
from twitterpibot.schedule.BlankTweetScheduledTask import BlankTweetScheduledTask
from twitterpibot.schedule.ConversationScheduledTask import ConversationScheduledTask
from twitterpibot.schedule.EdBallsDay import EdBallsDay
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
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask


def get_pi_scheduled_jobs(identity):
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
        ConversationResponse(identity),
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
        GifResponse(identity),
        FatherTedResponse(identity),
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
        return []

    def get_responses(self):
        followers = [
            andrewtathampi,
            andrewtathampi2
        ]
        return [HiveMindResponse(self, followers)]


andrewtatham = AndrewTathamIdentity()


class AndrewTathamPiIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(AndrewTathamPiIdentity, self).__init__(
            screen_name="andrewtathampi",
            id_str="2935295111",
            admin_identity=admin_identity)
        self.converse_with = "andrewtathampi2"
        self.colour = colorama.Fore.MAGENTA

    def get_tasks(self):
        return get_pi_tasks(self)

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPiIdentity, self).get_scheduled_jobs()
        jobs.extend(get_pi_scheduled_jobs(self))
        return jobs

    def get_responses(self):
        return get_pi_responses(self)


andrewtathampi = AndrewTathamPiIdentity(andrewtatham)


class AndrewTathamPi2Identity(BotIdentity):
    def __init__(self, admin_identity):
        super(AndrewTathamPi2Identity, self).__init__(
            screen_name="andrewtathampi2",
            id_str="3892161801",
            admin_identity=admin_identity)
        self.converse_with = "andrewtathampi"
        self.colour = colorama.Fore.CYAN

    def get_tasks(self):
        return get_pi_tasks(self)

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPi2Identity, self).get_scheduled_jobs()
        jobs.extend(get_pi_scheduled_jobs(self))
        return jobs

    def get_responses(self):
        return get_pi_responses(self)


andrewtathampi2 = AndrewTathamPi2Identity(andrewtatham)


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


numberwang_host = NumberwangHostIdentity(andrewtatham)


class JulieNumberwangIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(JulieNumberwangIdentity, self).__init__(
            screen_name="JulieNumberwang",
            id_str="4912246174",
            admin_identity=admin_identity)

    def get_tasks(self):
        return []


julienumberwang = JulieNumberwangIdentity(andrewtatham)


class SimonNumberwangIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(SimonNumberwangIdentity, self).__init__(
            screen_name="SimonNumberwang",
            id_str="4912203173",
            admin_identity=admin_identity)

    def get_tasks(self):
        return []


simonnumberwang = SimonNumberwangIdentity(andrewtatham)


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


eggpunbot = EggPunBotIdentity(andrewtatham)


class WhenIsInternationalMensDayBotIdentity(BotIdentity):
    def __init__(self, admin_identity):
        super(WhenIsInternationalMensDayBotIdentity, self).__init__(
            screen_name="WhenMensDay",
            id_str="708233017639215104",
            admin_identity=admin_identity)

    def get_scheduled_jobs(self):
        jobs = super(WhenIsInternationalMensDayBotIdentity, self).get_scheduled_jobs()
        jobs.append(WhenIsInternationalMensDayScheduledTask(self))
        return jobs

    def get_responses(self):
        return [WhenIsInternationalMensDayResponse(self)]


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

twitterpibot.run(all_identities)
