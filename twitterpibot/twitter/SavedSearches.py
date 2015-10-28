from twitterpibot.twitter import TwitterHelper
from multiprocessing import Lock
import datetime


_saved_searches = []
_lock = Lock()
_updated = None

def get_saved_searches():
    with _lock:

        if _updated: 
            delta = datetime.datetime.now() - _updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
        if not _updated or mins > 15:
            _update()

        return _saved_searches

def _update():
    global _saved_searches
    global _updated
    _saved_searches = TwitterHelper.get_saved_searches()
    _updated = datetime.datetime.now()
