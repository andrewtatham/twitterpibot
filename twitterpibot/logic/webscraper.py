import pprint
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


def _convert_unicode(unicode):
    unicode = unicode.replace("U+", "")
    unicode = unicode.zfill(8)
    unicode = "\\U" + unicode
    return unicode


def get_emojis():
    emoji = {}
    url = "http://www.unicode.org/emoji/charts/full-emoji-list.html"

    webpage = six.moves.urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, 'html.parser')
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                if len(cells) >= 15:
                    unicode = cells[1].text
                    name = cells[14].text
                    year = cells[15].text
                    year = re.match("[0-9]+", year).string[:4]
                    year = int(year)

                    if True:
                        # "," not in name \
                        #     and "Keycap" not in name \
                        #     and "Flag" not in name \
                        #     and year <= 2013:

                        if "≊" in name:
                            name = name[:name.index("≊")]

                        unicode = "".join((map(_convert_unicode, unicode.split(" "))))

                        name = name \
                            .replace(" ", "_") \
                            .replace("-", "_") \
                            .replace(".", "_") \
                            .replace(",", "_") \
                            .replace(":", "_") \
                            .replace("&", "_") \
                            .replace("'", "_") \
                            .replace("’", "_") \
                            .lower()
                        if name and unicode:
                            print("" + name + " = \"" + unicode + "\"")

    return emoji


def get_common_words():
    words = []
    url = "https://simple.wikipedia.org/wiki/Wikipedia:List_of_1000_basic_words"
    webpage = six.moves.urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, 'html.parser')
    for dd in soup.find_all('dd'):
        for a in dd.find_all("a"):
            word = a.get_text()
            word = word.lower().strip()
            words.append(word)
    words = set(words)
    return words


if __name__ == "__main__":
    pprint.pprint(get_emojis())
