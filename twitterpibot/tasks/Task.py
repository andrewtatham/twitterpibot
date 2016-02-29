import abc


class Task(object):
    def __init__(self, identity):
        self.identity = identity
        self.key = ""
        if identity:
            self.key += identity.screen_name + " "
        self.key += str(type(self))  # must be unique
        self.core = False

    @abc.abstractmethod
    def on_run(self):
        pass

    def on_stop(self):
        pass
