__author__ = 'andrewtatham'


def _map(mapping, letter):
    if letter in mapping:
        return mapping[letter]
    else:
        return letter