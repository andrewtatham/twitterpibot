from SongResponse import SongResponse
from PhotoResponse import PhotoResponse
from Magic8BallResponse import Magic8BallResponse
from RetweetResponse import RetweetResponse
from FatherTedResponse import FatherTedResponse
from MyTwitter import MyTwitter
from LoveResponse import LoveResponse
from BotBlockerResponse import BotBlockerResponse
from ThanksResponse import ThanksResponse
from HelloResponse import HelloResponse


class ResponseFactory(object):
    def __init__(self, context, *args, **kwargs):


        self.responses = [BotBlockerResponse(),
            PhotoResponse(),
            SongResponse(),
            ThanksResponse(),
            HelloResponse(),
            Magic8BallResponse(),
            FatherTedResponse(),
            LoveResponse(),
            RetweetResponse()]

        self.context = context
        for response in self.responses:
            response.context = self.context




    def Create(args, inboxItem):
        if inboxItem :
            for response in args.responses:
                if response.Condition(inboxItem):

                    if inboxItem.isTweet and response.Favourite(inboxItem):
                        with MyTwitter() as twitter:
                            twitter.create_favourite(id = inboxItem.status_id)

                    return response.Respond(inboxItem)

                    

        return None
        
