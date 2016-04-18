import colorama

from identity import Identity, BotIdentity
from twitterpibot import hardware
from twitterpibot.logic.april_fools_day import AprilFoolsDayScheduledTask
from twitterpibot.logic.botgle import BotgleResponse
from twitterpibot.logic.conversation import ConversationScheduledTask
from twitterpibot.logic.ed_balls_day import StreamEdBallsDayScheduledTask
from twitterpibot.logic.gender import WhenIsIMDScheduledTask, WhenIsInternationalMensDayResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
from twitterpibot.responses.EggPunResponse import EggPunResponse
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.HiveMindResponse import HiveMindResponse
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
from twitterpibot.responses.PhotoResponse import PhotoResponse
from twitterpibot.responses.ReplyResponse import ReplyResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.responses.SongResponse import SongResponse
from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
from twitterpibot.responses.x_or_y_response import X_Or_Y_Response
from twitterpibot.schedule.EggPunScheduledTask import EggPunScheduledTask
from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
from twitterpibot.schedule.common.LightsScheduledTask import LightsScheduledTask
from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask

__author__ = 'andrewtatham'


class AndrewTathamIdentity(Identity):
    def __init__(self):
        super(AndrewTathamIdentity, self).__init__(
            screen_name="andrewtatham",
            id_str="19201332")
        self.followers = None

    def get_responses(self):
        return [
            # HiveMindResponse(self, self.followers)
        ]


class AndrewTathamPiIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(AndrewTathamPiIdentity, self).__init__(
            screen_name="andrewtathampi",
            id_str="2935295111",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.MAGENTA
        self.converse_with = None

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPiIdentity, self).get_scheduled_jobs()
        jobs.extend([
            WikipediaScheduledTask(self),
            TalkLikeAPirateDayScheduledTask(self),
            WeatherScheduledTask(self),
            JokesScheduledTask(self),
            SongScheduledTask(self),
            ConversationScheduledTask(self, self.converse_with),
            HappyBirthdayScheduledTask(self),
            StreamEdBallsDayScheduledTask(self),
            AprilFoolsDayScheduledTask(self),
        ])

        if hardware.is_linux and (hardware.is_webcam_attached or hardware.is_picam_attached):
            jobs.extend([
                PhotoScheduledTask(self),
            ])
        if hardware.is_piglow_attached \
                or hardware.is_unicornhat_attached \
                or hardware.is_blinksticknano_attached:
            jobs.extend([
                LightsScheduledTask(self)
            ])
        return jobs

    def get_responses(self):
        responses = []
        responses.extend([
            SongResponse(self),
            TalkLikeAPirateDayResponse(self),
            X_Or_Y_Response(self),
            Magic8BallResponse(self),
        ])
        if hardware.is_picam_attached or hardware.is_webcam_attached:
            responses.extend([
                PhotoResponse(self),
            ])
        responses.extend([
            ReplyResponse(self),
            FavoriteResponse(self),
            RetweetResponse(self),
        ])
        responses.extend(super(AndrewTathamPiIdentity, self).get_responses())
        return responses


class AndrewTathamPi2Identity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(AndrewTathamPi2Identity, self).__init__(
            screen_name="andrewtathampi2",
            id_str="3892161801",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.CYAN
        self.converse_with = None

    def get_scheduled_jobs(self):
        jobs = super(AndrewTathamPi2Identity, self).get_scheduled_jobs()
        jobs.extend([
            WikipediaScheduledTask(self),
            TalkLikeAPirateDayScheduledTask(self),
            WeatherScheduledTask(self),
            JokesScheduledTask(self),
            SongScheduledTask(self),
            ConversationScheduledTask(self, self.converse_with),
            HappyBirthdayScheduledTask(self),
            # LocationScheduledTask(self),
            # RaiseExceptionScheduledTask(self),
            StreamEdBallsDayScheduledTask(self),
            AprilFoolsDayScheduledTask(self),
        ])

        if hardware.is_linux and (hardware.is_webcam_attached or hardware.is_picam_attached):
            jobs.extend([
                PhotoScheduledTask(self),
            ])
        if hardware.is_piglow_attached \
                or hardware.is_unicornhat_attached \
                or hardware.is_blinksticknano_attached:
            jobs.extend([
                LightsScheduledTask(self)
            ])
        return jobs

    def get_responses(self):
        responses = []
        responses.extend([

            SongResponse(self),
            TalkLikeAPirateDayResponse(self),
            # LocationResponse(self),
            X_Or_Y_Response(self),
            Magic8BallResponse(self),
        ])
        if hardware.is_picam_attached or hardware.is_webcam_attached:
            responses.extend([
                PhotoResponse(self),
            ])
        responses.extend([
            ReplyResponse(self),
            # FavoriteResponse(self),
            # RetweetResponse(self),
        ])
        responses.extend(super(AndrewTathamPi2Identity, self).get_responses())
        return responses


class NumberwangHostIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(NumberwangHostIdentity, self).__init__(
            screen_name="numberwang_host",
            id_str="4904547543",
            admin_identity=admin_identity)
        self.contestants = None

    def get_scheduled_jobs(self):
        jobs = super(NumberwangHostIdentity, self).get_scheduled_jobs()
        # noinspection PyTypeChecker
        jobs.extend([NumberwangHostScheduledTask(self, self.contestants)])
        return jobs


class JulieNumberwangIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(JulieNumberwangIdentity, self).__init__(
            screen_name="JulieNumberwang",
            id_str="4912246174",
            admin_identity=admin_identity)


class SimonNumberwangIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(SimonNumberwangIdentity, self).__init__(
            screen_name="SimonNumberwang",
            id_str="4912203173",
            admin_identity=admin_identity)


class EggPunBotIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(EggPunBotIdentity, self).__init__(
            screen_name="eggpunbot",
            id_str="706393659244154880",
            admin_identity=admin_identity)

        self.colour = colorama.Fore.YELLOW

    def get_scheduled_jobs(self):
        jobs = super(EggPunBotIdentity, self).get_scheduled_jobs()
        # noinspection PyTypeChecker
        jobs.extend([EggPunScheduledTask(self)])
        return jobs

    def get_responses(self):
        return [
            EggPunResponse(self)
        ]


class WhenIsInternationalMensDayBotIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(WhenIsInternationalMensDayBotIdentity, self).__init__(
            screen_name="WhenMensDay",
            id_str="708233017639215104",
            admin_identity=admin_identity)

    def get_scheduled_jobs(self):
        jobs = super(WhenIsInternationalMensDayBotIdentity, self).get_scheduled_jobs()
        # noinspection PyTypeChecker
        jobs.extend([WhenIsIMDScheduledTask(self)])
        return jobs

    def get_responses(self):
        return [WhenIsInternationalMensDayResponse(self)]


class BotgleArtistIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(BotgleArtistIdentity, self).__init__(
            screen_name="BotgleArtist",
            id_str="715477182106079232",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.GREEN

    def get_scheduled_jobs(self):
        jobs = super(BotgleArtistIdentity, self).get_scheduled_jobs()
        # jobs.extend([xxx(self)])
        return jobs

    def get_responses(self):
        return [BotgleResponse(self)]
