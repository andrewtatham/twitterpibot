from Response import Response
import os
from OutgoingDirectMessage import OutgoingDirectMessage
import time
class RestartResponse(Response):
    def Condition(args, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
            and inboxItem.sender.screen_name == "andrewtatham" \
            and "restart" in inboxItem.words and not args.context.hardware.iswindows
    def Respond(args, inboxItem):
        
        args.context.outbox.put(OutgoingDirectMessage(replyTo = inboxItem, text="Going down..."))
        time.sleep(2)
        os.system("cd ~; ./twitter")
        

        
