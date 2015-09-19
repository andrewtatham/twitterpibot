import sys
class Task(object):
    def __init__(self, *args, **kwargs):
        self.context = None
        self.enabled = True
        return super(Task, self).__init__(*args, **kwargs)

    def onInit(args):
        pass

    def onRun(args):
        pass

    def onStop(args):
        pass
