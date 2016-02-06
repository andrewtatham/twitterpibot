from pymarkov import markov

ply = 3
length = 20


class MarkovResult(object):
    def __init__(self, markov_dict):
        self.markov_dict = markov_dict

    def speak(self):
        return markov.generate(self.markov_dict, length, ply)


def train(text):
    return MarkovResult(markov.train(text, ply))
