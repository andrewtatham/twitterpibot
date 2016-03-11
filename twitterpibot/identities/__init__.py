import abc

import colorama

from twitterpibot.identities.statistics import Statistics
from twitterpibot.schedule.FollowScheduledTask import FollowScheduledTask
from twitterpibot.schedule.MidnightScheduledTask import MidnightScheduledTask
from twitterpibot.schedule.MonitorScheduledTask import MonitorScheduledTask
from twitterpibot.schedule.SubscribedListsScheduledTask import SubscribedListsScheduledTask
from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter.twitterhelper import TwitterHelper
from twitterpibot.users.lists import Lists
from twitterpibot.users.users import Users


class Identity(object):
    def __init__(self, screen_name, id_str, ):
        self.screen_name = screen_name
        self.id_str = id_str
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
    def __init__(self, screen_name, id_str, admin_identity):
        super(BotIdentity, self).__init__(screen_name, id_str)
        self.admin_identity = admin_identity

    def get_tasks(self):
        return [
            StreamTweetsTask(self)
        ]

    def get_scheduled_jobs(self):
        return [
            MonitorScheduledTask(self),
            MidnightScheduledTask(self),
            UserListsScheduledTask(self, self.admin_identity),
            SubscribedListsScheduledTask(self, self.admin_identity),
            FollowScheduledTask(self),
        ]

    def get_responses(self):
        return []
