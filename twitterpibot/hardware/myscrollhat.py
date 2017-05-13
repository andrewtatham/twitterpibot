import logging
import scrollphathd
import time
from scrollphathd.fonts import font5x7smoothed

q = []
status_length = 0

scrollphathd.rotate(degrees=180)
scrollphathd.clear()
scrollphathd.show()


def lights():
    global status_length
    if status_length > 0:
        scrollphathd.show()
        scrollphathd.scroll(1)
        status_length -= 1
        time.sleep(0.1)
    else:
        time.sleep(1)

    if status_length <= 0 and any(q):
        status = q.pop()
        scrollphathd.write_string(status, font=font5x7smoothed, brightness=0.1)
        status_length = scrollphathd.write_string(status, x=0, y=0, font=font5x7smoothed, brightness=0.1)


def inbox_item_received(inbox_item):
    logging.info("myscrollhat inbox_item_received {}".format(inbox_item))
    if inbox_item.is_tweet or inbox_item.is_direct_message:
        logging.info("myscrollhat text {}".format(inbox_item.text))
        q.insert(0, inbox_item.text)


def close():
    logging.info("myscrollhat close")
    scrollphathd.clear()
    scrollphathd.show()
