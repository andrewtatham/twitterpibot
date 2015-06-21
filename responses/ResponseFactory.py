from HelpResponse import HelpResponse
from SongResponse import SongResponse
from PhotoResponse import PhotoResponse
from Magic8BallResponse import Magic8BallResponse

class ResponseFactory(object):
    def __init__(self, *args, **kwargs):


        self.responses = [HelpResponse(),
                          PhotoResponse(),
                          SongResponse(),
                          Magic8BallResponse()]

        self.context = kwargs['context']
        for response in self.responses:
            response.context = self.context




    def Create(args, inboxItem):
        if inboxItem is not None:
            for response in args.responses:
                if response.Condition(inboxItem):
                    return response.Respond(inboxItem)

        return None
        
