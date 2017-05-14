import logging
import scrollphathd
import time
from scrollphathd.fonts import font5x7smoothed

logger = logging.getLogger(__name__)

q = []
status_length = 0

scrollphathd.rotate(degrees=180)
scrollphathd.clear()
scrollphathd.show()


def lights():
    global status_length
    if status_length > 0:
        logger.info("myscrollhat status_length = {}".format(status_length))
        scrollphathd.show()
        scrollphathd.scroll(1)
        status_length -= 1
        time.sleep(0.05)
    else:
        time.sleep(2)

    if status_length <= 0 and any(q):
        scrollphathd.clear()
        scrollphathd.show()
        logger.info("myscrollhat len(q) = {}".format(len(q)))
        status = 6 * " " + q.pop() + 6 * " "
        status_length = scrollphathd.write_string(status, x=0, y=0, font=font5x7smoothed, brightness=0.1)


def inbox_item_received(inbox_item):
    logger.info("myscrollhat inbox_item_received {}".format(inbox_item))
    if inbox_item.is_tweet or inbox_item.is_direct_message:
        logger.info("myscrollhat text {}".format(inbox_item.text))
        q.insert(0, inbox_item.short_description())


def close():
    logger.info("myscrollhat close")
    scrollphathd.clear()
    scrollphathd.show()
