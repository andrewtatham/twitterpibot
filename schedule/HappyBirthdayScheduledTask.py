from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import Birthdays

class HappyBirthdayScheduledTask(ScheduledTask):

    #def GetTrigger(args):
    #    return CronTrigger(hour = "8-20/2")

    def onRun(args):
        birthdayUsers = Birthdays.GetBirthdayUsers()
        if birthdayUsers:
            for birthdayUser in birthdayUsers:
                Birthdays.SingBirthdaySong(birthdayUser)


    




