from identity import Identity
from twitterpibot.responses.HiveMindResponse import HiveMindResponse
from twitterpibot.schedule.common.UserListsScheduledTask import UserListsScheduledTask


class AndrewTathamIdentity(Identity):
    def __init__(self, stream):
        super(AndrewTathamIdentity, self).__init__(
            screen_name="andrewtatham",
            id_str="19201332",
            stream=stream)
        self.buddies = None

    def get_scheduled_jobs(self):
        jobs = super().get_scheduled_jobs()
        jobs.append(UserListsScheduledTask(self, None))
        return jobs

    def get_responses(self):
        responses = super(AndrewTathamIdentity, self).get_responses()
        responses.extend([HiveMindResponse(self, self.buddies)])
        return responses