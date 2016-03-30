import os

from twitterpibot.logic import fsh

__author__ = 'andrewtatham'

botgle_dictionary_path = fsh.root + os.sep + "twitterpibot" + os.sep + "text" + os.sep + "boggle_advanced.txt"


def get_botgle_candidates(letters):
    letters = set(letters)
    with open(botgle_dictionary_path) as file:
        words = file.readlines()
    words = list(map(lambda word: word.upper().strip(), words))
    words = list(filter(lambda word: len(word) >= 3, words))
    words = list(filter(lambda word: set(word) < letters, words))
    return words


if __name__ == '__main__':
    get_botgle_candidates("CAT")
