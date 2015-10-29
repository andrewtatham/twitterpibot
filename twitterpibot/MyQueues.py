try:
    from queue import Queue
except ImportError:
    # noinspection PyUnresolvedReferences
    from Queue import Queue

inbox = Queue()

