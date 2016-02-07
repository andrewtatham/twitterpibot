import re

import six

from bs4 import BeautifulSoup


def get_malcolm_tucker_quotes():
    quotes = []
    url = "https://en.wikiquote.org/wiki/The_Thick_of_It"
    rx = re.compile("^Malcolm( Tucker)?: ?|\[.*\] ?")
    webpage = six.moves.urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, 'html.parser')
    for element in soup.find_all('dd'):
        text = element.get_text()

        if text.startswith("Malcolm"):
            text = rx.sub(string=text, repl="")
            quotes.append(text)
    return quotes

if __name__ == "__main__":
    get_malcolm_tucker_quotes()
