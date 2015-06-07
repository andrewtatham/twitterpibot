from InboxItem import InboxItem

class IncomingEvent(InboxItem):
    def __init__(self, data):
        # https://dev.twitter.com/streaming/overview/messages-types#Events_event
        event = data["event"]
        sourceID = data["source"]["id_str"]
        sourceName = data["source"]["name"]
        sourceScreenName = data["source"]["screen_name"]

        targetID = data["target"]["id_str"]
        targetName = data["target"]["name"]
        targetScreenName = data["target"]["screen_name"]
                
        eventinfo = "EVENT: " + event \
                    + " SOURCE: " + sourceName + " [" + sourceScreenName + "]" \
                    + " TARGET: " + targetName + " [" + targetScreenName + "]"
        logging.info(eventinfo)
                
        if data["event"] == "follow":
            pass
        elif data["event"] == "unfollow":
            pass
        else:
            logging.info(data)


    def IsEvent(args):
        return True