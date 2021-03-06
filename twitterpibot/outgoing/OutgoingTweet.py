import logging

from twitterpibot.outgoing.OutboxTextItem import OutboxTextItem

logger = logging.getLogger(__name__)


class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, reply_to=None, text=None,
                 in_reply_to_id_str=None,
                 file_paths=None,
                 location=None,
                 quote=None,
                 urls=None
                 ):

        super(OutgoingTweet, self).__init__()

        self.filePaths = file_paths
        self.location = location
        self.media_ids = []
        self.urls = []
        self.mentions = []
        if urls:
            self.urls.extend(urls)
        self.quote_url = None

        self._determine_reply(in_reply_to_id_str, reply_to)
        self.status = text
        self._determine_quote(quote)

    def _determine_reply(self, in_reply_to_id_str, reply_to):
        if in_reply_to_id_str:
            self.in_reply_to_id_str = in_reply_to_id_str
        elif reply_to and reply_to.is_tweet and reply_to.id_str:
            self.in_reply_to_id_str = reply_to.id_str

        if reply_to:
            if reply_to.sender.screen_name:
                self.mentions.append(reply_to.sender.screen_name)
                if reply_to.mentions:
                    for to_screen_name in reply_to.mentions:
                        if to_screen_name != reply_to.sender.screen_name:
                            self.mentions.append(to_screen_name)

    def display(self):
        logger.info("-> Tweet: " + self.status)
        if self.quote_url:
            logger.info("-> quote_url: {}".format(self.quote_url))
        if self.urls:
            for url in self.urls:
                logger.info("-> url: {}".format(url))
        if self.location:
            logger.info("-> Location: {}".format(self.location.get_display_name()))
        if self.filePaths:
            logger.info("-> filePaths: {}".format(self.filePaths))

    def _determine_quote(self, quote):
        if quote:
            quote_url = "https://twitter.com/{}/status/{}".format(quote.sender.screen_name, quote.id_str)
            self.quote_url = quote_url
