import os

folder = "twitterpibot" + os.sep + "text" + os.sep


def get_text(text_name):
    file = open(folder + text_name + os.extsep + "txt")
    text = file.readlines()
    file.close()
    return text
