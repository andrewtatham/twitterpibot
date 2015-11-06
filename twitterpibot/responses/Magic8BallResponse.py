import random

from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class Magic8BallResponse(Response):
    def __init__(self):
        self.responses = ['Signs point to yes.',
                          'Yes.',
                          'Reply hazy, try again.',
                          'Without a doubt.',
                          'My sources say no.',
                          'As I see it, yes.',
                          'You may rely on it.',
                          'Concentrate and ask again.',
                          'Outlook not so good.',
                          'It is decidedly so.',
                          'Better not tell you now.',
                          'Very doubtful.',
                          'Yes - definitely.',
                          'It is certain.',
                          'Cannot predict now.',
                          'Most likely.',
                          'Ask again later.',
                          'My reply is no.',
                          'Outlook good.',
                          'Don\'t count on it.',
                          'Yes, in due time.',
                          'My sources say no.',
                          'Definitely not.',
                          'Yes.',
                          'You will have to wait.',
                          'I have my doubts.',
                          'Outlook so so.',
                          'Looks good to me!',
                          'Who knows?',
                          'Looking good!',
                          'Probably.',
                          'Are you kidding?',
                          'Go for it!',
                          'Don\'t bet on it.',
                          'Forget about it.']

    def condition(self, inbox_item):
        return super(Magic8BallResponse, self).condition(inbox_item) \
               and inbox_item.text.find("?") != -1

    def respond(self, inbox_item):
        response = random.choice(self.responses) + " #Magic8Ball"
        reply_with(inbox_item=inbox_item, text=response)
