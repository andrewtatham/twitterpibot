import datetime

from twitterpibot.twitter import twitterhelper

_saved_searches = []
_updated = None


def get_saved_searches(identity):
    if _updated:
        delta = datetime.datetime.now() - _updated
        mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
        if mins > 15:
            _update(identity)
    else:
        _update(identity)

    return _saved_searches


def _update(identity):
    global _saved_searches
    global _updated
    _saved_searches = twitterhelper.get_saved_searches(identity)
    _updated = datetime.datetime.now()
