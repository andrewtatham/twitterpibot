import datetime
import logging
import pprint

logger = logging.getLogger(__name__)


class Conversation(object):
    def __init__(self, conversation_key):
        self.conversation_key = conversation_key
        self.tweet_tree = {}
        self.tweet_descriptions = {}
        self.root_id = None
        self._updated = None

    def incoming(self, inbox_item):
        if inbox_item.in_reply_to_id_str:
            if inbox_item.in_reply_to_id_str in self.tweet_tree:
                self.tweet_tree[inbox_item.in_reply_to_id_str].append(inbox_item.id_str)
            else:
                self._ensure_root_id(inbox_item.in_reply_to_id_str)
                self.tweet_tree[inbox_item.in_reply_to_id_str] = [inbox_item.id_str]
            self.tweet_descriptions[inbox_item.id_str] = \
                "incoming {} @{} replied {}".format(inbox_item.sender.name, inbox_item.sender.screen_name,
                                                    inbox_item.text)

        else:

            self._ensure_root_id(inbox_item.id_str)
            self.tweet_tree[inbox_item.id_str] = []
            self.tweet_descriptions[inbox_item.id_str] = \
                "incoming {} @{} tweeted {}".format(inbox_item.sender.name, inbox_item.sender.screen_name,
                                                    inbox_item.text)
        self._updated = datetime.datetime.now()

    def outgoing(self, identity, outbox_item):

        if outbox_item.in_reply_to_id_str:

            if outbox_item.in_reply_to_id_str not in self.tweet_tree:
                self.tweet_tree[outbox_item.in_reply_to_id_str] = [outbox_item.id_str]
            else:
                self._ensure_root_id(outbox_item.in_reply_to_id_str)
                self.tweet_tree[outbox_item.in_reply_to_id_str].append(outbox_item.id_str)
            self.tweet_descriptions[outbox_item.id_str] = \
                "outgoing @{} replied {}".format(identity.screen_name, outbox_item.status)

        else:
            self._ensure_root_id(outbox_item.id_str)
            self.tweet_tree[outbox_item.id_str] = []
            self.tweet_descriptions[outbox_item.id_str] = \
                "outgoing @{} tweeted {}".format(identity.screen_name, outbox_item.status)

        self._updated = datetime.datetime.now()

    def display(self):
        logger.info("conversation {} length {}".format(self.conversation_key, self.length()))
        logger.info(pprint.pformat(self.tweet_tree))
        if self.root_id:
            logger.info("root id = " + str(self.root_id))
            self._display(self.root_id)

    def _display(self, tweet_id, level=0):
        desc = self.tweet_descriptions.get(tweet_id)
        line = ">" * level + " " + tweet_id + " " + str(desc)
        logger.info(line)
        if tweet_id in self.tweet_tree:
            for child_id in self.tweet_tree[tweet_id]:
                self._display(child_id, level + 1)

    def length(self):
        return len(self.tweet_tree)

    def last_updated(self):
        return self._updated

    def _ensure_root_id(self, id_str):
        if not self.root_id:
            self.root_id = id_str


class ConversationHelper(object):
    def __init__(self, identity):
        self._identity = identity
        self._conversations = dict()
        self._id_keys = dict()

    def _determine_conversation_key(self, inbox_item=None, outbox_item=None):
        if inbox_item:

            # todo, retweets, favourites, events esp favourited, DM's
            if inbox_item.is_tweet:

                # todo quote tweets
                if inbox_item.in_reply_to_id_str and inbox_item.in_reply_to_id_str in self._id_keys:
                    # replied
                    return self._id_keys[inbox_item.in_reply_to_id_str]
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
                    key = "{} {}".format(self._identity.screen_name, outbox_item.id_str)
                    self._id_keys[outbox_item.id_str] = key
                    return key

        return None

    def incoming(self, inbox_item):
        conversation_key = self._determine_conversation_key(inbox_item=inbox_item)
        if conversation_key:
            if conversation_key not in self._conversations:
                self._conversations[conversation_key] = Conversation(conversation_key=conversation_key)
            conversation = self._conversations[conversation_key]
            conversation.incoming(inbox_item=inbox_item)
            if conversation.length() > 1:
                conversation.display()
            return self._conversations[conversation_key]

    def outgoing(self, outbox_item):
        conversation_key = self._determine_conversation_key(outbox_item=outbox_item)
        if conversation_key:
            if conversation_key not in self._conversations:
                self._conversations[conversation_key] = Conversation(conversation_key=conversation_key)
            conversation = self._conversations[conversation_key]
            conversation.outgoing(identity=self._identity, outbox_item=outbox_item)
            if conversation.length() > 1:
                self._conversations[conversation_key].display()
            return self._conversations[conversation_key]

    def housekeep(self):
        limit = datetime.datetime.now() + datetime.timedelta(hours=-1)
        delete_us = list([k for k, v in self._conversations.items() if v.last_updated() and v.last_updated() < limit])
        logger.info("removing {} conversations ".format(len(delete_us)))
        for k in delete_us:
            self._conversations.pop(k, None)
        logger.info("tracking {} conversations".format(len(self._conversations)))
