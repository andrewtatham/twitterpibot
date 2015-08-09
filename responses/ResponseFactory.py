from HelpResponse import HelpResponse
from SongResponse import SongResponse
from PhotoResponse import PhotoResponse
from Magic8BallResponse import Magic8BallResponse
from FavouriteResponse import FavouriteResponse
from RetweetResponse import RetweetResponse

class ResponseFactory(object):
    def __init__(self, context, *args, **kwargs):


        self.responses = [HelpResponse(),
                          PhotoResponse(),
                          SongResponse(),
                          Magic8BallResponse(),
                          FavouriteResponse(),
                          RetweetResponse()]

        self.context = context
        for response in self.responses:
            response.context = self.context




    def Create(args, inboxItem):
        if inboxItem :
            for response in args.responses:
                if response.Condition(inboxItem):
                    return response.Respond(inboxItem)

        return None
        
