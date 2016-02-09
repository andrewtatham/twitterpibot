from twython.api import Twython

import twitterpibot.twitter.Authenticator as Authenticator

_tokens = None
_screen_name = None
_instance = None


class MyTwitter(object):
    def __init__(self, screen_name=None):
        global _screen_name
        if not _screen_name:
            if not screen_name:
                raise Exception("_screen_name is required on first use")
            else:
                _screen_name = screen_name

    def __enter__(self):
        global _tokens
        global _instance
        if not _tokens:
            global _screen_name
            _tokens = Authenticator.get_tokens(_screen_name)
        if not _instance:
            _instance = Twython(_tokens[0], _tokens[1], _tokens[2], _tokens[3])
        return _instance

    def __exit__(self, *args, **kwargs):
        pass
