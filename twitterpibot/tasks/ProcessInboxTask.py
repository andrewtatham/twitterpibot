import logging

from twitterpibot.responses.ResponseFactory import ResponseFactory
from twitterpibot.tasks.Task import Task
import twitterpibot.incoming.InboxItemFactory as InboxItemFactory
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.Statistics import RecordIncomingTweet, RecordIncomingDirectMessage
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
                        RecordIncomingTweet()
                    if type(inbox_item) is IncomingDirectMessage:
                        RecordIncomingDirectMessage()
                    _process_inbox_item(self, inbox_item)
        except Exception:
            if data:
                logger.warn(data)
            raise
        finally:
            twitterpibot.MyQueues.inbox.task_done()

    def onStop(self):
        twitterpibot.MyQueues.inbox.put(None)


def _process_inbox_item(args, inbox_item):
    inbox_item.display()

    hardware.on_inbox_item_received(inbox_item)

    response = args.responseFactory.create(inbox_item)
    if response:
        send(response)
