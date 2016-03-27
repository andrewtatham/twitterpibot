import pprint

__author__ = 'andrewtatham'


def get_botgle_candidates(letters):
    letters = set(letters)
    with open("words.txt") as file:
        words = file.readlines()
    words = list(map(lambda word: word.upper().strip(), words))
    words = list(filter(lambda word: len(word) >= 3, words))
    words = list(filter(lambda word: set(word) < letters, words))
    return words


if __name__ == '__main__':
    get_botgle_candidates("CAT")
