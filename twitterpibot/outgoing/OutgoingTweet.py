from twitterpibot.outgoing.OutboxTextItem import OutboxTextItem
import logging
logger = logging.getLogger(__name__)


class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, replyTo=None, text=None, in_reply_to_status_id=None, filePaths=None):

        super(OutgoingTweet, self).__init__()

        if in_reply_to_status_id:
            self.in_reply_to_status_id = in_reply_to_status_id
        elif replyTo and replyTo.isTweet and replyTo.status_id:
            self.in_reply_to_status_id = replyTo.status_id

        self.filePaths = filePaths

        self.status = ''

        if replyTo:
            if replyTo.sender.screen_name:
                self.status += '@' + replyTo.sender.screen_name + ' '
            if replyTo.targets:
                for to_screen_name in replyTo.targets:
                    if to_screen_name != replyTo.sender.screen_name:
                        self.status += '@' + to_screen_name + ' '

        if text:
            self.status = self.status + text

    def Display(self):
        logger.info("-> Tweet: " + self.status)
