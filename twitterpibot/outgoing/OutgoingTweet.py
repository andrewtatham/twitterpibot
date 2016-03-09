from twitterpibot.outgoing.OutboxTextItem import OutboxTextItem
import logging
logger = logging.getLogger(__name__)


class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, reply_to=None, text=None, in_reply_to_status_id=None, file_paths=None):

        super(OutgoingTweet, self).__init__()

        if in_reply_to_status_id:
            self.in_reply_to_status_id = in_reply_to_status_id
        elif reply_to and reply_to.is_tweet and reply_to.status_id:
            self.in_reply_to_status_id = reply_to.status_id

        self.filePaths = file_paths

        self.status = ''

        if reply_to:
            self.status += '.'
            if reply_to.sender.screen_name:
                self.status += '@' + reply_to.sender.screen_name + ' '
            if reply_to.targets:
                for to_screen_name in reply_to.targets:
                    if to_screen_name != reply_to.sender.screen_name:
                        self.status += '@' + to_screen_name + ' '

        if text:
            self.status += text

    def display(self):
        logger.info("-> Tweet: " + self.status)
