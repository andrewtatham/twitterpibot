import logging

from twitterpibot.responses.ResponseFactory import ResponseFactory
from twitterpibot.tasks.Task import Task
import twitterpibot.incoming.InboxItemFactory as InboxItemFactory
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.Statistics import record_incoming_tweet, record_incoming_direct_message
from twitterpibot.twitter.TwitterHelper import send
import twitterpibot.hardware.hardware as hardware
import twitterpibot.MyQueues

logger = logging.getLogger(__name__)


class ProcessInboxTask(Task):
    def __init__(self):
        Task.__init__(self)
        self.core = True
        self.responseFactory = ResponseFactory()

    def onRun(self):
        data = None
        try:
            data = twitterpibot.MyQueues.inbox.get()
            if data:
                inbox_item = InboxItemFactory.create(data)
                if inbox_item:
                    if type(inbox_item) is IncomingTweet:
                        record_incoming_tweet()
                    if type(inbox_item) is IncomingDirectMessage:
                        record_incoming_direct_message()
                    _process_inbox_item(self, inbox_item)
            else:
                logger.info("None in inbox, exiting")
        except Exception:
            if data:
                logger.warn(data)
            raise
        finally:
            twitterpibot.MyQueues.inbox.task_done()

    def onStop(self):
        logger.info("putting None in inbox")
        twitterpibot.MyQueues.inbox.put(None)
        logger.info("put None in inbox")


def _process_inbox_item(args, inbox_item):
    inbox_item.display()

    hardware.on_inbox_item_received(inbox_item)

    response = args.responseFactory.create(inbox_item)
    if response:
        send(response)
