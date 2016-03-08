import abc


class Task(object):
    def __init__(self, identity, key=None):
        self.identity = identity
        self.key = ""
        if identity:  # must be unique
            self.key += identity.screen_name + " "
        if key:
            self.key += key
        else:
            self.key += str(type(self))
        self.core = False

    @abc.abstractmethod
    def on_run(self):
        pass

    def on_stop(self):
        pass
