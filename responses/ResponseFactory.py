from HelpResponse import HelpResponse
class ResponseFactory(object):
    def __init__(self, *args, **kwargs):
        self.responses = [HelpResponse()]



    def Create(args, inboxItem):
        if inboxItem is not None:
            for response in args.responses:
                if response.Condition(inboxItem):
                    return response.Respond(inboxItem)

        return None
        
