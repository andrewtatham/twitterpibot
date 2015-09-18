from Response import Response
from OutgoingDirectMessage import OutgoingDirectMessage
import time
import datetime
from subprocess import call
import os
class RestartResponse(Response):
    def Condition(args, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
            and inboxItem.sender.screen_name == "andrewtatham" \
            and "restart" in inboxItem.words and not args.context.hardware.iswindows
    def Respond(args, inboxItem):
        
        args.context.outbox.put(OutgoingDirectMessage(
            replyTo = inboxItem, 
            text="Down... " + str(datetime.datetime.now())))
        time.sleep(2)
        subprocess.call("sh twitter", shell=True)
        #os.system("sh ./twitter")
        

        
