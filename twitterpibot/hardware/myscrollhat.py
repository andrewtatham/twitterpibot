import logging

import datetime
import scrollphathd
import time
from scrollphathd.fonts import font5x7smoothed

logger = logging.getLogger(__name__)
scroll_until_x = 18
q = [
    str(datetime.datetime.now()),
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
    status = 6 * " " + q.pop() + 6 * " "
    status_length = scrollphathd.write_string(status, x=0, y=0, font=font5x7smoothed, brightness=0.1)
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
        time.sleep(2)


def inbox_item_received(inbox_item):
    if inbox_item.is_tweet or inbox_item.is_direct_message:
        enqueue(inbox_item.short_display())


def on_lights_scheduled_task():
    enqueue(str(datetime.datetime.now()))


def close():
    scrollphathd.clear()
    scrollphathd.show()
