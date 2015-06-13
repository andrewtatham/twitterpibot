class Task(object):
    def __init__(self, *args, **kwargs):
        self.Context = None
        self.enabled = True
        return super(Task, self).__init__(*args, **kwargs)

    def onInit(args):
        print('Task.onInit')

    def onRun(args):
        print('Task.onRun')

    def onStop(args):
        print('Task.onStop')
