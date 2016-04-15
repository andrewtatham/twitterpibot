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
                    name = cells[14].text
                    year = cells[15].text
                    year = re.match("[0-9]+", year).string[:4]
                    year = int(year)

                    if "," not in name \
                            and "Keycap" not in name \
                            and "Flag" not in name \
                            and year <= 2013:

                        if "≊" in name:
                            name = name[:name.index("≊")]

                        val = "\\N{" + name + "}"
                        name = name \
                            .replace(" ", "_") \
                            .replace("-", "_") \
                            .replace(".", "_") \
                            .replace("&", "_") \
                            .replace("'", "_") \
                            .replace("’", "_") \
                            .lower()
                        if name and val:
                            print("" + name + " = \"" + val + "\"")

    return emoji


if __name__ == "__main__":
    get_emojis()
