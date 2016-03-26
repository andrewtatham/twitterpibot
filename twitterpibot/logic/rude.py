import pprint
from twitterpibot.logic import urlhelper

if __name__ == '__main__':
    params = {"term": "alabama hot pocket"}
    url = "http://api.urbandictionary.com/v0/define"
    url = urlhelper.parameterise(params, url)
    response = urlhelper.get_response(url)
    pprint.pprint(response)
