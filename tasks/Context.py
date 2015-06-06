from Queue import Queue
class Context(object):
    def __init__(self, *args, **kwargs):
        self.inbox = Queue()
        self.outbox = Queue()

    def GetStatus(args):
        return args.inbox.qsize()

