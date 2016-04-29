import os
from collections import Counter

from twitterpibot.logic import fsh


class DictionaryEntry(object):
    def __init__(self, word):
        self.word = word.upper().strip()
        self.set = set(self.word)
        self.length = len(self.word)
        self.count = Counter(self.word)


__author__ = 'andrewtatham'
# /Users/andrewtatham/twitterpibot/twitterpibot/text/boggle_advanced.txt
botgle_dictionary_path = fsh.root + "twitterpibot" + os.sep + "text" + os.sep + "boggle_advanced" + os.extsep + "txt"
words = fsh.readlines(botgle_dictionary_path)
words = list(map(lambda word: DictionaryEntry(word), words))
boggle_words = list(filter(lambda word: word.length >= 5, words))


def get_botgle_candidates(letters):
    letters = set(letters)
    botgle_candidates = list(
        map(lambda entry: entry.word, filter(lambda entry: entry.set.issubset(letters), boggle_words)))
    return botgle_candidates


def _is_proper_subset(entry, letters_set, letters_length, letters_count):
    return entry.length == letters_length and entry.set.issubset(letters_set) and entry.count == letters_count


def get_anagram_candidates(letters):
    letters = letters.upper()
    letters_length = len(letters)
    letters_count = Counter(letters)
    letters_set = set(letters)
    anagram_candidates = list(map(lambda entry: entry.word, filter(lambda entry: _is_proper_subset(
        entry=entry,
        letters_length=letters_length,
        letters_count=letters_count,
        letters_set=letters_set), words)))
    return anagram_candidates


if __name__ == '__main__':
    print(get_botgle_candidates("BANANAS"))
    print(get_anagram_candidates("AlistBintAnus"))
