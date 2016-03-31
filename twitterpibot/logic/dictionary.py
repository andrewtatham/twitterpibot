import os

from twitterpibot.logic import fsh

__author__ = 'andrewtatham'
# /Users/andrewtatham/twitterpibot/twitterpibot/text/boggle_advanced.txt
botgle_dictionary_path = fsh.root + "twitterpibot" + os.sep + "text" + os.sep + "boggle" + os.extsep + "txt"
words = fsh.readlines(botgle_dictionary_path)
words = list(map(lambda word: word.upper().strip(), words))
boggle_words = list(filter(lambda word: len(word) >= 3, words))
boggle_sets = list(map(lambda word: (word, set(word)), words))


def get_botgle_candidates(letters):
    letters = set(letters)
    words = list(map(lambda tuple: tuple[0], filter(lambda tuple: tuple[1].issubset(letters), boggle_sets)))
    return words


if __name__ == '__main__':
    print(get_botgle_candidates("BANANA"))
