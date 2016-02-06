from twitterpibot.logic import markovhelper
from twitterpibot.movies import moviehelper
from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class MovieMarkovResponse(Response):
    def __init__(self, movie_name):
        movie_lines = moviehelper.get_lines(movie_name)
        self.markov = markovhelper.train(movie_lines)

    def condition(self, inbox_item):
        return super(MovieMarkovResponse, self).reply_condition(inbox_item)

    def respond(self, inbox_item):
        reply_with(inbox_item=inbox_item, text=self.markov.speak())
