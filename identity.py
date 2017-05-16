import abc

import colorama

import twitterpibot.hardware.myhardware
from twitterpibot.logic import conversation_helper
from twitterpibot.logic.admin_commands import ImportTokensResponse, ExportTokensResponse, DropCreateTablesResponse, \
    RestartResponse, SetTokenResponse
from twitterpibot.logic.ed_balls_day import TweetEdBallsDayScheduledTask
from twitterpibot.logic.statstics import Statistics
from twitterpibot.schedule.PhotoScheduledTask import PhotoScheduledTask
from twitterpibot.schedule.common.IdentityMonitorScheduledTask import IdentityMonitorScheduledTask
from twitterpibot.schedule.common.SubscribedListsScheduledTask import SubscribedListsScheduledTask
from twitterpibot.schedule.common.SuggestedUsersScheduledTask import SuggestedUsersScheduledTask
from twitterpibot.schedule.common.UserListsScheduledTask import UserListsScheduledTask
from twitterpibot.schedule.common.ratelimitsscheduledtask import RateLimitsScheduledTask
from twitterpibot.schedule.common.usersscheduledtasks import ManageUsersScheduledTask, ScoreUsersScheduledTask, \
    GetUsersScheduledTask, UpdateUserGroupsScheduledTask, ManageListMembersScheduledTask
from twitterpibot.schedule.responses_scheduled_task import ResponsesScheduledTask
from twitterpibot.tasks.StreamTweetsTask import StreamTweetsTask
from twitterpibot.twitter import twitterhelper
from twitterpibot.users import users

__author__ = 'andrewtatham'


class Identity(object):
    def __init__(self, screen_name, id_str, stream=True):
        self.id_str = id_str
        self.screen_name = screen_name
        self.profile_url = "https://twitter.com/" + self.screen_name
        self.admin_screen_name = "andrewtatham"
        self.colour = colorama.Fore.WHITE
        self.tokens = None
        self._stream = stream
        self.streamer = None

        self.name = None
        self.description = None
        self.location = None
        self.profile_banner_url = None
        self.profile_image_url = None
        self.url = None

        self.following_count = None
        self.followers_count = None
        self.statuses_count = None
        self.favourites_count = None

        self.twitter = twitterhelper.TwitterHelper(self)

        self.users = users.Users(self)
        self.statistics = Statistics()
        self.conversations = conversation_helper.ConversationHelper(self)
        self.converse_with = None
        self.facebook = None

    def update(self, me):
        self.id_str = me["id_str"]
        self.name = me["name"]
        self.description = me["description"]
        self.location = me["location"]
        self.profile_banner_url = me["profile_banner_url"]
        if self.profile_banner_url:
            self.profile_banner_url += "/300x100"

        self.profile_image_url = me["profile_image_url"]
        self.url = me["url"]

        self.following_count = me["friends_count"]
        self.followers_count = me["followers_count"]
        self.statuses_count = me["statuses_count"]
        self.favourites_count = me["favourites_count"]

    @abc.abstractmethod
    def get_tasks(self):
        tasks = []
        if self._stream:
            tasks.append(StreamTweetsTask(self))
        return tasks

    @abc.abstractmethod
    def get_scheduled_jobs(self):
        return [
            TweetEdBallsDayScheduledTask(self),
            SuggestedUsersScheduledTask(self),
            GetUsersScheduledTask(self),
            ScoreUsersScheduledTask(self),
            RateLimitsScheduledTask(self),
            UpdateUserGroupsScheduledTask(self)

        ]

    @abc.abstractmethod
    def get_responses(self):
        return [
        ]


class BotIdentity(Identity):
    def __init__(self, screen_name, id_str, admin_identity):
        super(BotIdentity, self).__init__(screen_name, id_str)
        self.admin_identity = admin_identity

    def get_scheduled_jobs(self):
        jobs = super(BotIdentity, self).get_scheduled_jobs()
        jobs.extend([
            IdentityMonitorScheduledTask(self),
            UserListsScheduledTask(self, self.admin_identity),
            SubscribedListsScheduledTask(self, self.admin_identity),
            ManageUsersScheduledTask(self),
            ManageListMembersScheduledTask(self),
            ResponsesScheduledTask(self)
        ])
        if twitterpibot.hardware.myhardware.is_linux and (
                    twitterpibot.hardware.myhardware.is_webcam_attached or
                    twitterpibot.hardware.myhardware.is_picam_attached):
            jobs.append(PhotoScheduledTask(self))

        return jobs

    def get_responses(self):
        responses = super(BotIdentity, self).get_responses()
        responses.extend([
            RestartResponse(self),
            ImportTokensResponse(self),
            SetTokenResponse(self),
            ExportTokensResponse(self),
            DropCreateTablesResponse(self),
        ])
        return responses
