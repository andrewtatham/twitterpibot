import markovgen

import identities_pis
from twitterpibot.logic import webscraper, feedhelper
from twitterpibot.movies import moviehelper
from twitterpibot.songs import songhelper
from twitterpibot.topics.topichelper import get_topics


class MarkovWrapper(object):
    def __init__(self, text=None):
        self.markov_dict = markovgen.Markov()
        if text:
            self.markov_dict.feed(text)

    def speak(self):
        return self.markov_dict.generate_markov_text()

    def train(self, text):
        self.markov_dict.feed(text)


def get(text=None):
    return MarkovWrapper(text)


if __name__ == "__main__":
    sep = " "  # os.linesep
    markov = get()
    identity = identities_pis.AndrewTathamPiIdentity(None)
    list_name = "Arseholes"
    tweets = identity.twitter.get_list_statuses(
        list_id=identity.users.lists._list_ids[list_name],
        slug=list_name,
        owner_screen_name=identity.screen_name,
        owner_id=identity.id_str,
        count=200)
    tweets = list(map(lambda tweet: tweet["text"], tweets))
    markov.train(sep.join(tweets))
    markov.train(sep.join(webscraper.get_malcolm_tucker_quotes()))
    markov.train(sep.join(feedhelper.get_news_stories()))
    markov.train(sep.join(moviehelper.get_lines("matrix")))
    markov.train(sep.join(moviehelper.get_lines("dodgeball")))
    # markov.train(sep.join(textfilehelper.get_text("ulysees")))
    for key in songhelper.keys():
        markov.train(sep.join(songhelper.get_song(key)["lyrics"]))

    for i in range(25):
        text = markov.speak()
        topics = get_topics(text)

        print(text)
        if topics:
            print(topics)
