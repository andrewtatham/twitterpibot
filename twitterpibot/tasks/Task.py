import abc


class Task(object):
    def __init__(self):
        self.key = str(type(self))
        self.core = False

    @abc.abstractmethod
    def on_run(self):
        pass

    def on_stop(self):
        pass
