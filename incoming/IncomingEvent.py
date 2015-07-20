from InboxItem import InboxItem

class IncomingEvent(InboxItem):
    def __init__(self, data, context):
        
        super(IncomingEvent, self).__init__(data)

        self.isEvent = True

        # https://dev.twitter.com/streaming/overview/messages-types#Events_event
        self.event = data["event"]
        self.sourceID = data["source"]["id_str"]
        self.sourceName = data["source"]["name"]
        self.sourceScreenName = data["source"]["screen_name"]

        self.targetID = data["target"]["id_str"]
        self.targetName = data["target"]["name"]
        self.targetScreenName = data["target"]["screen_name"]

        
  

    def Display(args):
        
        text = "* Event: " + args.event \
                    + " Source: " + args.sourceName + " [" + args.sourceScreenName + "]" \
                    + " Target: " + args.targetName + " [" + args.targetScreenName + "]"
        print(text)