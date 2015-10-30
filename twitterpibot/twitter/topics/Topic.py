import re


class Topic(object):
    def __init__(self, regexes):
        self.rx = re.compile("|".join(regexes), re.IGNORECASE)

    def condition(self, text):
        return self.rx.match(text)

    def __str__(self):
        return self.__class__.__name__

