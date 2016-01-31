import random

import wikipedia


def GetRandomPage():
    # https://wikipedia.readthedocs.org/en/latest/quickstart.html
    rand = wikipedia.random(pages=1)
    page = None
    while not page:
        try:
            page = wikipedia.page(title=rand)
        except wikipedia.PageError:
            rand = wikipedia.random(pages=1)
            page = None
        except wikipedia.DisambiguationError as e:
            rand = random.choice(e.options)
            page = None
    return page
