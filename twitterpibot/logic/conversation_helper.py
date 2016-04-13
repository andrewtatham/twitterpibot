import datetime
import logging
import pprint

logger = logging.getLogger(__name__)


class Conversation(object):
    def __init__(self, conversation_key):
        self.conversation_key = conversation_key
        self.tweets = {}
        self._updated = None

    def incoming(self, inbox_item):
        if inbox_item.in_reply_to_id_str:
            if inbox_item.in_reply_to_id_str in self.tweets:
                self.tweets[inbox_item.in_reply_to_id_str].append(inbox_item.id_str)
            else:
                self.tweets[inbox_item.in_reply_to_id_str] = [inbox_item.id_str]
        else:
            self.tweets[inbox_item.id_str] = []
        self._updated = datetime.datetime.now()

    def outgoing(self, outbox_item, sent_tweet_id, in_reply_to_id_str):
        if in_reply_to_id_str:
            if in_reply_to_id_str not in self.tweets:
                self.tweets[in_reply_to_id_str] = [sent_tweet_id]
            else:
                self.tweets[in_reply_to_id_str].append(sent_tweet_id)
        else:
            self.tweets[sent_tweet_id] = []
        self._updated = datetime.datetime.now()

    def display(self):
        l = self.length()
        logger.info("{} length {}".format(self.conversation_key, l))
        if l > 1:
            logger.info(pprint.pformat(self.tweets))

    def length(self):
        return len(self.tweets)

    def last_updated(self):
        return self._updated


class ConversationHelper(object):
    def __init__(self, identity):
        self._identity = identity
        self._conversations = dict()
        self._id_keys = dict()

    def _determine_conversation_key(self, inbox_item=None, outbox_item=None):
        if inbox_item:

            # todo, events esp favourited, DM's
            if inbox_item.is_tweet:

                # todo quote tweets
                if inbox_item.in_reply_to_id_str and inbox_item.in_reply_to_id_str in self._id_keys:
                    # replied
                    return self._id_keys[inbox_item.in_reply_to_id_str]
                elif inbox_item.retweeted_status and inbox_item.retweeted_status.id_str in self._id_keys:
                    # retweeted
                    return self._id_keys[inbox_item.retweeted_status.id_str]
                elif inbox_item.id_str in self._id_keys:
                    # incoming new (dont think this could happen?)
                    return self._id_keys[inbox_item.id_str]
                else:
                    # incoming new
                    key = "{} {}".format(self._identity.screen_name, inbox_item.id_str)
                    self._id_keys[inbox_item.id_str] = key
                    return key

        elif outbox_item:

            if outbox_item.is_tweet:

                if outbox_item.in_reply_to_id_str and outbox_item.in_reply_to_id_str in self._id_keys:
                    # replied
                    return self._id_keys[outbox_item.in_reply_to_id_str]
                else:
                    # outgoing new
                    key = "{} {}".format(self._identity.screen_name, outbox_item.str_id)
                    self._id_keys[outbox_item.str_id] = key
                    return key

        return None

    def incoming(self, inbox_item):
        conversation_key = self._determine_conversation_key(inbox_item)
        if conversation_key:
            if conversation_key not in self._conversations:
                self._conversations[conversation_key] = Conversation(conversation_key=conversation_key                                                                     )
            else:
                self._conversations[conversation_key].incoming(inbox_item=inbox_item)

            self._conversations[conversation_key].display()
            return self._conversations[conversation_key]

    def outgoing(self, outbox_item, sent_tweet_id, in_reply_to_id_str):
        conversation_key = self._determine_conversation_key(outbox_item)
        if conversation_key:
            if conversation_key not in self._conversations:
                self._conversations[conversation_key] = Conversation(conversation_key=conversation_key
                                                                     )
            else:
                self._conversations[conversation_key].outgoing(outbox_item=outbox_item,
                                                               sent_tweet_id=sent_tweet_id,
                                                               in_reply_to_id_str=in_reply_to_id_str)
            self._conversations[conversation_key].display()
            return self._conversations[conversation_key]

    def housekeep(self):
        limit = datetime.datetime.now() + datetime.timedelta(hours=-1)
        for k in self._conversations:
            last_updated = self._conversations[k].last_updated()
            if last_updated and last_updated < limit:
                logger.info("removing conversation " + k)
                self._conversations.pop(k, None)
