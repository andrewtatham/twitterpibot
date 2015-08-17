from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
import os
from UserList import UserList
import logging


class UserListsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return super(UserListsScheduledTask, args).GetTrigger()

    def onInit(args):
        args.UpdateUserLists()


    def onRun(args):
        args.UpdateUserLists()


    def UpdateUserLists(args):
        logging.info("updating user lists")
        with MyTwitter() as twitter:
        
            lists2 = []
            lists1 = twitter.show_owned_lists()
            for list in lists1["lists"]:
                logging.info("updating user list " + list["id_str"] + " " + list["name"])
                members = twitter.get_list_members(list_id = list["id_str"])
                lists2.append(UserList(list, members))
        
        args.context.users.lists = lists2