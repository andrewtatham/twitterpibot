import os
import pprint

import markovgen

from twitterpibot.logic import webscraper


class MarkovResult(object):
    def __init__(self, markov_dict):
        self.markov_dict = markov_dict

    def speak(self):
        return self.markov_dict.generate_markov_text()


def train(text):
    markov_dict = markovgen.Markov()
    markov_dict.feed(text)
    # pprint.pprint(markov_dict.generate_markov_text())
    return MarkovResult(markov_dict)


if __name__ == "__main__":
    pprint.pprint(train(os.linesep.join(webscraper.get_malcolm_tucker_quotes())).speak())
