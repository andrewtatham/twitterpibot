from Response import Response
from OutgoingDirectMessage import OutgoingDirectMessage
import time
import datetime
from subprocess import call
import os
import subprocess
import MyUI
class RestartResponse(Response):
    def Condition(self, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
            and inboxItem.sender.screen_name == "andrewtatham" \
            and "restart" in inboxItem.words # and not hardware.iswindows
    def Respond(self, inboxItem):
        MyUI.Close()
        

        
