import abc

import colorama

from twitterpibot.logic import conversation_helper
from twitterpibot.logic.ed_balls_day import TweetEdBallsDayScheduledTask
from twitterpibot.logic.statstics import Statistics
from twitterpibot.schedule.FollowScheduledTask import FollowScheduledTask
from twitterpibot.schedule.MonitorScheduledTask import IdentityMonitorScheduledTask
from twitterpibot.schedule.SubscribedListsScheduledTask import SubscribedListsScheduledTask
from twitterpibot.schedule.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter import twitterhelper
from twitterpibot.users import users, lists

__author__ = 'andrewtatham'


class Identity(object):
    def __init__(self, screen_name, id_str):
        self.screen_name = screen_name
        self.id_str = id_str
        self.admin_screen_name = "andrewtatham"
        self.tokens = None
        self.streamer = None
        self.twitter = twitterhelper.TwitterHelper(self)
        self.converse_with = None
        self.users = users.Users(self)
        self.following = set()
        self.colour = colorama.Fore.WHITE
        self.profile_image_url = None
        self.statistics = Statistics()
        self.lists = lists.Lists(self)
        self.conversations = conversation_helper.ConversationHelper(self)

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
            UserListsScheduledTask(self, self.admin_identity),
            SubscribedListsScheduledTask(self, self.admin_identity),
            FollowScheduledTask(self),

        ])
        return jobs

    def get_responses(self):
        return []