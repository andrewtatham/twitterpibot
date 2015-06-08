from Queue import Queue
class Context(object):
    def __init__(self, *args, **kwargs):
        self.inbox = Queue()
        self.outbox = Queue()
        self.song = Queue()

    def GetStatus(args):

        status = Status()
        status.inboxCount = args.inbox.qsize()
        status.outboxCount = args.outbox.qsize()
        status.songCount = args.song.qsize()

        return status


class Status(object):
    pass