import webbrowser

from twitterpibot.data_access import dal
from twitterpibot.hardware import myhardware

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

from twython.api import Twython
import logging

logger = logging.getLogger(__name__)


def get_tokens(screen_name):
    app_key = dal.get_token("twitter app key " + screen_name)
    app_secret = dal.get_token("twitter app secret " + screen_name)

    final_key = dal.get_token("twitter final key " + screen_name)
    final_secret = dal.get_token("twitter final secret " + screen_name)

    if not final_key or not final_secret:
        twitter = Twython(app_key, app_secret)
        auth = twitter.get_authentication_tokens()
        oauth_token = auth["oauth_token"]
        oauth_token_secret = auth["oauth_token_secret"]
        url = auth["auth_url"]

        logger.info(url)
        if myhardware.is_andrew_desktop or myhardware.is_andrew_macbook:
            webbrowser.open(url)
        oauth_verifier = input("Please enter your pin:")

        twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        final_key = final_step["oauth_token"]
        final_secret = final_step["oauth_token_secret"]

        dal.set_token("twitter final key " + screen_name, final_key)
        dal.set_token("twitter final secret " + screen_name, final_secret)

    tokens = [app_key, app_secret, final_key, final_secret]

    return tokens
