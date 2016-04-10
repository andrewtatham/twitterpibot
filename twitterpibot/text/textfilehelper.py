import os
from twitterpibot.logic import fsh

folder = fsh.root + "twitterpibot" + os.sep + "text" + os.sep


def get_text(text_name):
    file = open(folder + text_name + os.extsep + "txt")
    text = file.readlines()
    text = list(filter(lambda line: bool(line), text))
    text = list(map(lambda line: line.strip(), text))
    file.close()
    return text
