import os
from twitterpibot.logic import fsh

folder = fsh.root + "twitterpibot" + os.sep + "text" + os.sep


def get_text(text_name=None, path=None):
    if not path:
        path = folder + text_name + os.extsep + "txt"

    file = open(path)
    text = file.readlines()
    text = list(filter(lambda line: bool(line), text))
    text = list(map(lambda line: line.strip(), text))
    file.close()
    return text
