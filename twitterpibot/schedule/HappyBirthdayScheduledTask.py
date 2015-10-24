from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import twitterpibot.processing.Birthdays as Birthdays


class HappyBirthdayScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour="8-20/2")

    def onRun(self):
        birthdayUsers = Birthdays.GetBirthdayUsers()
        if birthdayUsers:
            for birthdayUser in birthdayUsers:
                Birthdays.SingBirthdaySong(birthdayUser)
