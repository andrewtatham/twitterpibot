from twython.api import Twython

import Authenticator

_tokens = None
_screen_name = None


class MyTwitter(object):
    def __init__(self, screen_name=None):
        global _screen_name
        _screen_name = screen_name

    def __enter__(self):
        global _tokens

        if not _tokens:
            global _screen_name
            _tokens = Authenticator.GetTokens(_screen_name)

        instance = Twython(_tokens[0], _tokens[1], _tokens[2], _tokens[3])
        return instance

    def __exit__(self, *args, **kwargs):
        pass
