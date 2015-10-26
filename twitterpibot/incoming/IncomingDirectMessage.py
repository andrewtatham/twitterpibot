from twitterpibot.incoming.InboxTextItem import InboxTextItem
import twitterpibot.users.Users as Users
import logging
logger = logging.getLogger(__name__)


class IncomingDirectMessage(InboxTextItem):
    # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages
    # https://dev.twitter.com/rest/reference/get/direct_messages
    def __init__(self, data):
        super(IncomingDirectMessage, self).__init__()
        self.isDirectMessage = True
        self.sender = Users.getUser(data=data["direct_message"]["sender"])
        self.recipient = Users.getUser(data=data["direct_message"]["recipient"])
        self.from_me = self.sender.isMe
        self.to_me = self.recipient.isMe
        self.targets = [self.sender.screen_name]
        self.text = data["direct_message"]["text"]
        self.words = self.text.split()

    def Display(self):
        text = u" * DM from @" + self.sender.screen_name + u" to @" + self.recipient.screen_name + u": " + self.text
        logger.info(text)
