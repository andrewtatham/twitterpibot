import random


class Response(object):
    def condition(self, inbox_item):
        return (inbox_item.isDirectMessage or inbox_item.isTweet) \
               and not inbox_item.from_me \
               and (inbox_item.to_me and (not inbox_item.isReplyLess or random.randint(0, 3) == 0)
                    or (inbox_item.sender.isBot and random.randint(0, 3) == 0)
                    or (inbox_item.sender.isFriend and random.randint(0, 1) == 0)
                    or (inbox_item.sender.isRetweetMore and random.randint(0, 9) == 0)
                    or random.randint(0, 99) == 0)

    def favourite(self, inbox_item):
        return False

    def contains(self, list, item):
        if list:
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False

    def respond(self, inbox_item):
        return None
