from Queue import Queue
from Cameras import Cameras
from MyPiglow import MyPiglow
class Context(object):
    def __init__(self, *args, **kwargs):
        self.inbox = Queue()
        self.outbox = Queue()
        self.song = Queue()


        self.cameras = Cameras()
        self.piglow = MyPiglow()

    def GetStatus(args):

        status = Status()
        status.inboxCount = args.inbox.qsize()
        status.outboxCount = args.outbox.qsize()
        status.songCount = args.song.qsize()

        return status


class Status(object):
    pass