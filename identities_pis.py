import colorama

from twitterpibot.hardware import myhardware
from identity import Identity, BotIdentity
from twitterpibot.facebook import facebook_helper
from twitterpibot.logic.anagram_solver import AnagramBotResponse
from twitterpibot.logic.april_fools_day import AprilFoolsDayScheduledTask
from twitterpibot.logic.botgle import BotgleResponse
from twitterpibot.logic.conversation import ConversationScheduledTask
from twitterpibot.logic.cypher_game import CypherHostMidnightScheduledTask, CypherHostScheduledTask, CypherHostResponse, \
    DecypherScheduledTask, DecypherResponse
from twitterpibot.logic.ed_balls_day import TweetBeforeEdBallsDayScheduledTask, StreamEdBallsDayScheduledTask
from twitterpibot.logic.gender import WhenIsIMDScheduledTask, WhenIsInternationalMensDayResponse
from twitterpibot.logic.morse_code import MorseCodeResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask, NumberwangHostResponse
from twitterpibot.responses.EggPunResponse import EggPunResponse
from twitterpibot.responses.FavoriteResponse import FavoriteResponse
from twitterpibot.responses.HiveMindResponse import HiveMindResponse
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse
from twitterpibot.responses.PhotoResponse import PhotoResponse
from twitterpibot.responses.ReplyResponse import ReplyResponse
from twitterpibot.responses.RetweetResponse import RetweetResponse
from twitterpibot.responses.TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse
from twitterpibot.responses.weather_response import WeatherResponse
from twitterpibot.responses.x_or_y_response import X_Or_Y_Response
from twitterpibot.schedule.EggPunScheduledTask import EggPunScheduledTask
from twitterpibot.schedule.HappyBirthdayScheduledTask import HappyBirthdayScheduledTask
from twitterpibot.schedule.JokesScheduledTask import JokesScheduledTask
from twitterpibot.schedule.JudgementDayScheduledTask import JudgementDayScheduledTask
from twitterpibot.schedule.PokemonScheduledTask import PokemonScheduledTask
from twitterpibot.schedule.SongScheduledTask import SongScheduledTask
from twitterpibot.schedule.TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
from twitterpibot.schedule.WeatherScheduledTask import WeatherScheduledTask
from twitterpibot.schedule.WikipediaScheduledTask import WikipediaScheduledTask
from twitterpibot.schedule.announcement_scheduled_task import AnnouncementScheduledTask
from twitterpibot.schedule.common.UserListsScheduledTask import UserListsScheduledTask

__author__ = 'andrewtatham'


class AndrewTathamIdentity(Identity):
    def __init__(self):
        super(AndrewTathamIdentity, self).__init__(
            screen_name="andrewtatham",
            id_str="19201332")
        self.buddies = None

    def get_scheduled_jobs(self):
        jobs = super().get_scheduled_jobs()
        jobs.append(UserListsScheduledTask(self, None))
        return jobs

    def get_responses(self):
        responses = super(AndrewTathamIdentity, self).get_responses()
        responses.extend([HiveMindResponse(self, self.buddies)])
        return responses


class PiIdentity(BotIdentity):
    def __init__(self, screen_name, id_str, admin_identity):
        super(PiIdentity, self).__init__(screen_name, id_str, admin_identity)
        self.converse_with = None

    def get_scheduled_jobs(self):
        jobs = super(PiIdentity, self).get_scheduled_jobs()
        jobs.extend([
            WikipediaScheduledTask(self),
            TalkLikeAPirateDayScheduledTask(self),
            WeatherScheduledTask(self),
            JokesScheduledTask(self),
            SongScheduledTask(self),
            HappyBirthdayScheduledTask(self),
            # LocationScheduledTask(self),
            # RaiseExceptionScheduledTask(self),
            TweetBeforeEdBallsDayScheduledTask(self),
            StreamEdBallsDayScheduledTask(self),
            AprilFoolsDayScheduledTask(self),
            JudgementDayScheduledTask(self),
            DecypherScheduledTask(self),
            ConversationScheduledTask(self, self.converse_with),
            PokemonScheduledTask(self, self.converse_with)
        ])

        return jobs

    def get_responses(self):
        responses = super(PiIdentity, self).get_responses()
        responses.extend([
            TalkLikeAPirateDayResponse(self),
            AnagramBotResponse(self),
            MorseCodeResponse(self),
            DecypherResponse(self),
            # LocationResponse(self),
            WeatherResponse(self),
            X_Or_Y_Response(self),
            Magic8BallResponse(self),
        ])
        if myhardware.is_picam_attached or myhardware.is_webcam_attached:
            responses.append(PhotoResponse(self))
        responses.extend([
            ReplyResponse(self),
            FavoriteResponse(self),
            RetweetResponse(self),
        ])
        responses.extend(super(PiIdentity, self).get_responses())
        return responses


class AndrewTathamPiIdentity(PiIdentity):
    def __init__(self, admin_identity=None):
        super(AndrewTathamPiIdentity, self).__init__(
            screen_name="andrewtathampi",
            id_str="2935295111",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.MAGENTA
        self.facebook = facebook_helper.FacebookHelper(self)

    def get_scheduled_jobs(self):
        jobs = super().get_scheduled_jobs()
        jobs.append(AnnouncementScheduledTask(self))
        return jobs


class AndrewTathamPi2Identity(PiIdentity):
    def __init__(self, admin_identity=None):
        super(AndrewTathamPi2Identity, self).__init__(
            screen_name="andrewtathampi2",
            id_str="3892161801",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.CYAN


class NumberwangHostIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(NumberwangHostIdentity, self).__init__(
            screen_name="numberwang_host",
            id_str="4904547543",
            admin_identity=admin_identity)
        self.contestant_pairs = None

    def get_responses(self):
        responses = super(NumberwangHostIdentity, self).get_responses()
        responses.extend([NumberwangHostResponse(self, self.contestant_pairs)])
        return responses

    def get_scheduled_jobs(self):
        jobs = super(NumberwangHostIdentity, self).get_scheduled_jobs()
        # noinspection PyTypeChecker
        jobs.extend([NumberwangHostScheduledTask(self, self.contestant_pairs)])
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

    def get_responses(self):
        return [BotgleResponse(self)]


class TheMachinesCodeIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(TheMachinesCodeIdentity, self).__init__(
            screen_name="THEMACHINESCODE",
            id_str="723742144645718016",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.GREEN

    def get_scheduled_jobs(self):
        jobs = super(TheMachinesCodeIdentity, self).get_scheduled_jobs()
        # noinspection PyTypeChecker
        jobs.extend([
            CypherHostMidnightScheduledTask(self),
            CypherHostScheduledTask(self)
        ])
        return jobs

    def get_responses(self):
        responses = super(TheMachinesCodeIdentity, self).get_responses()
        # noinspection PyTypeChecker
        responses.extend([
            CypherHostResponse(self)
        ])
        return responses


