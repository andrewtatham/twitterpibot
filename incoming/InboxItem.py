
class InboxItem(object):
    def __init__(self, *args, **kwargs):
        self.from_me = False
        self.to_me = False


        return super(InboxItem, self).__init__(*args, **kwargs)


    def Display(args):
        print('InboxItem.Display')

    def IsTweet(args):
        return False;

    def IsDirectMessage(args):
        return False;

    def IsEvent(args):
        return False;
