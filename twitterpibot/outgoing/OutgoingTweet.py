import logging

from twitterpibot.outgoing.OutboxTextItem import OutboxTextItem

logger = logging.getLogger(__name__)


class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, reply_to=None, text=None,
                 in_reply_to_id_str=None,
                 file_paths=None,
                 location=None):

        super(OutgoingTweet, self).__init__()

        self.filePaths = file_paths
        self.location = location

        self.status = ''
        self._determine_reply(in_reply_to_id_str, reply_to)
        self.status += text

    def _determine_reply(self, in_reply_to_id_str, reply_to):
        if in_reply_to_id_str:
            self.in_reply_to_id_str = in_reply_to_id_str
        elif reply_to and reply_to.is_tweet and reply_to.id_str:
            self.in_reply_to_id_str = reply_to.id_str
        if reply_to:
            self.status += '.'
            if reply_to.sender.screen_name:
                self.status += '@' + reply_to.sender.screen_name + ' '
            if reply_to.targets:
                for to_screen_name in reply_to.targets:
                    if to_screen_name != reply_to.sender.screen_name:
                        self.status += '@' + to_screen_name + ' '

    def display(self):
        logger.info("-> Tweet: " + self.status)
        if self.location:
            logger.info("-> Location: " + self.location.get_display_name())
        if self.filePaths:
            logger.info("-> filePaths: " + str(self.filePaths))

