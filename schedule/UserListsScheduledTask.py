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
        
            newLists = []
            myLists = twitter.show_owned_lists()
            for myList in myLists["lists"]:
                text = "updating user list " + myList["id_str"] + " " + myList["name"]
                print(text)
                logging.info(text)
                members = twitter.get_list_members(list_id = myList["id_str"])

                newList = UserList(list = myList, members = members)
                newLists.append(newList)
        
        args.context.users.updateLists(lists = newLists)