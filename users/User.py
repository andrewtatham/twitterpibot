class User(object):
    def __init__(self, id, lists, *args, **kwargs):

        self.isBot = False
        self.isRetweetLess = False
        self.IsRetweetMore = False

        



        for list in lists:
            if id in list.members:
                if list.name == "Retweet Less":
                    self.isRetweetLess = True
                elif list.name == "Retweet More":
                    self.IsRetweetMore = True
                elif list.name == "Awesome Bots":
                    self.isBot = True
                else:
                    pass
        


        return super(User, self).__init__(*args, **kwargs)