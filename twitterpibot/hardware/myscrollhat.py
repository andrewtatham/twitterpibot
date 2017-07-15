import logging

import datetime
import scrollphathd
import time
from scrollphathd.fonts import font5x7smoothed

from twitterpibot.responses.Response import _one_in

logger = logging.getLogger(__name__)
scroll_until_x = 0
q = [
    datetime.datetime.now().strftime("%x"),  # Date
    datetime.datetime.now().strftime("%X"),  # Time
    "Hello World"
]

status_length = 0

scrollphathd.rotate(degrees=180)
scrollphathd.clear()
scrollphathd.show()


def enqueue(text):
    logger.info("_enqueue text = {}".format(text))
    q.insert(0, text)


def _dequeue():
    global status_length
    scrollphathd.clear()
    logger.info("len(q) = {}".format(len(q)))
    status = q.pop()
    status_length = scrollphathd.write_string(status, x=18, y=0, font=font5x7smoothed, brightness=0.1) + 17
    scrollphathd.show()
    time.sleep(0.01)


def _scroll():
    global status_length
    scrollphathd.scroll(1)
    status_length -= 1
    scrollphathd.show()
    time.sleep(0.01)


def _scroll_finished():
    return status_length <= scroll_until_x


def lights():
    if not _scroll_finished():
        _scroll()
    elif _scroll_finished() and any(q):
        _dequeue()
    else:
        scrollphathd.clear()
        enqueue(datetime.datetime.now().strftime("%X"))  # Time
        scrollphathd.show()
        time.sleep(0.25)


def inbox_item_received(inbox_item):
    if inbox_item.is_tweet and inbox_item.text_stripped_whitespace_removed and not any(inbox_item.medias) and _one_in(10):
        enqueue(inbox_item.short_display())
    elif inbox_item.is_direct_message:
        enqueue(inbox_item.short_display())


def on_lights_scheduled_task():
    enqueue(datetime.datetime.now().strftime("%x"))  # Date
    enqueue(datetime.datetime.now().strftime("%X"))  # Time

def close():
    scrollphathd.clear()
    scrollphathd.show()
