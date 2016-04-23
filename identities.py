import colorama

from identity import Identity, BotIdentity, PiIdentity
from twitterpibot.logic.botgle import BotgleResponse
from twitterpibot.logic.cypher_game import CypherHostMidnightScheduledTask, CypherHostScheduledTask, CypherHostResponse
from twitterpibot.logic.gender import WhenIsIMDScheduledTask, WhenIsInternationalMensDayResponse
from twitterpibot.logic.numberwang import NumberwangHostScheduledTask
from twitterpibot.responses.EggPunResponse import EggPunResponse
from twitterpibot.schedule.EggPunScheduledTask import EggPunScheduledTask

__author__ = 'andrewtatham'


class AndrewTathamIdentity(Identity):
    def __init__(self):
        super(AndrewTathamIdentity, self).__init__(
            screen_name="andrewtatham",
            id_str="19201332")
        self.followers = None


class AndrewTathamPiIdentity(PiIdentity):
    def __init__(self, admin_identity=None):
        super(AndrewTathamPiIdentity, self).__init__(
            screen_name="andrewtathampi",
            id_str="2935295111",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.MAGENTA


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
