from Response import Response
import os
class RestartResponse(Response):
    def Condition(args, inboxItem):
        return inboxItem.isDirectMessage and not inboxItem.from_me and inboxItem.to_me \
            and inboxItem.sender.screen_name == "andrewtatham" \
            and "restart" in inboxItem.words
    def Respond(args, inboxItem):
        os.system("sh ~/twitter")
        

        
