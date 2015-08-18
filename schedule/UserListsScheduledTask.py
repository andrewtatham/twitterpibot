from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
import os
from UserList import UserList
import logging
from apscheduler.triggers.cron import CronTrigger


class UserListsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(minute="5/15")

    #def onInit(args):
    #    args.UpdateUserLists()


    def onRun(args):
        args.UpdateUserLists()


    def UpdateUserLists(args):
        print("updating user lists")
        logging.info("updating user lists")
        with MyTwitter() as twitter:
        
            lists2 = []
            lists1 = twitter.show_owned_lists()
            for list in lists1["lists"]:
                text = "updating user list " + list["id_str"] + " " + list["name"]
                print(text)
                logging.info(text)
                members = twitter.get_list_members(list_id = list["id_str"])
                lists2.append(UserList(list, members))
        
        args.context.users.lists = lists2