class Task(object):
    def __init__(self):
        self.key = str(type(self))
        self.core = False

    def onRun(self):
        pass

    def onStop(self):
        pass
