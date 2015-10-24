import random


class Response(object):
    def Condition(self, inbox_item):
        return not inbox_item.from_me and (inbox_item.isDirectMessage or not (not inbox_item.isTweet or not (
            inbox_item.to_me and (not inbox_item.sender.isReplyLess or random.randint(0, 9) == 0) or (
                inbox_item.sender.isBot and random.randint(0, 3) == 0) or (
                inbox_item.sender.isFriend and random.randint(0, 1) == 0) or (
                inbox_item.sender.isRetweetMore and random.randint(0, 9) == 0) or random.randint(0, 99) == 0)))

    def Favourite(self, inbox_item):
        return False

    def Contains(self, list, item):
        if list:
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False

    def Respond(self, inbox_item):
        return None
