import os

from twitterpibot.logic import fsh

__author__ = 'andrewtatham'
# /Users/andrewtatham/twitterpibot/twitterpibot/text/boggle_advanced.txt
botgle_dictionary_path = fsh.root + "twitterpibot" + os.sep + "text" + os.sep + "boggle_advanced" + os.extsep + "txt"
words = fsh.readlines(botgle_dictionary_path)
words = list(map(lambda word: word.upper().strip(), words))
boggle_words = list(filter(lambda word: len(word) >= 5, words))
boggle_sets = list(map(lambda word: (word, set(word)), boggle_words))


def get_botgle_candidates(letters):
    letters = set(letters)
    botgle_candidates = list(map(lambda t: t[0], filter(lambda t: t[1].issubset(letters), boggle_sets)))
    return botgle_candidates


if __name__ == '__main__':
    print(get_botgle_candidates("BANANA"))
