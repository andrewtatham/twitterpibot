import datetime
import os

__author__ = 'andrewtatham'


class Statistics(object):
    def __init__(self):
        self._stats = {}

    def reset(self):
        self._stats = {}

    def increment(self, key):
        if key not in self._stats:
            self._stats[key] = 0
        self._stats[key] += 1

    def get_statistics(self):
        text = "Stats at " + datetime.datetime.now().strftime("%x %X") + os.linesep
        for key, val in self._stats.items():
            text += str(val) + " " + key + os.linesep
        return text

    def record_incoming_tweet(self, tweet):
        self.increment("Incoming Tweets")

    def record_incoming_direct_message(self, dm):
        self.increment("Incoming Direct Messages")

    def record_incoming_event(self, event):
        self.increment("Incoming Event")

    def record_connection(self):
        self.increment("Connnections")

    def record_outgoing_tweet(self):
        self.increment("Outgoing Tweets")

    def record_outgoing_direct_message(self):
        self.increment("Outgoing Direct Messages")

    def record_outgoing_song_lyric(self):
        self.increment("Outgoing Song Lyrics")

    def record_warning(self):
        self.increment("Warnings")

    def record_error(self):
        self.increment("Errors")

    def record_retweet(self):
        self.increment("Retweets")

    def record_favourite(self):
        self.increment("Favourites")
