import datetime
import logging
import os
import pprint

logger = logging.getLogger(__name__)


class Conversation(object):
    def __init__(self, conversation_key):
        self.conversation_key = conversation_key
        self.tweet_tree = {}
        self.tweet_descriptions = {}
        self.root_id = None
        self._updated = None
        self._responses = []

    def incoming(self, inbox_item):

        if inbox_item.in_reply_to_id_str:
            action = "replied"
            if inbox_item.in_reply_to_id_str in self.tweet_tree:
                self.tweet_tree[inbox_item.in_reply_to_id_str].append(inbox_item.id_str)
            else:
                self._ensure_root_id(inbox_item.in_reply_to_id_str)
                self.tweet_tree[inbox_item.in_reply_to_id_str] = [inbox_item.id_str]
        elif inbox_item.quoted_status_id_str:
            action = "quoted"
            if inbox_item.quoted_status_id_str in self.tweet_tree:
                self.tweet_tree[inbox_item.quoted_status_id_str].append(inbox_item.id_str)
            else:
                self._ensure_root_id(inbox_item.quoted_status_id_str)
                self.tweet_tree[inbox_item.quoted_status_id_str] = [inbox_item.id_str]

        else:
            action = "tweeted"
            self._ensure_root_id(inbox_item.id_str)
            self.tweet_tree[inbox_item.id_str] = []

        self.tweet_descriptions[inbox_item.id_str] = "incoming {} @{} {} {}".format(
            inbox_item.sender.name,
            inbox_item.sender.screen_name,
            action,
            inbox_item.text)
        self._updated = datetime.datetime.now()

        if self._responses:
            for response in self._responses:
                response(inbox_item)

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
        text = []
        if self.root_id:
            self._display(self.root_id, level=0, text=text)
        return os.linesep.join(text)

    def _display(self, tweet_id, level, text):
        desc = self.tweet_descriptions.get(tweet_id)
        if desc:
            desc = desc.replace(os.linesep, " ")
        line = ">" * level + " " + str(desc)
        text.append(line)
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

    def add_response(self, response):
        self._responses.append(response)


class ConversationHelper(object):
    def __init__(self, identity):
        self._identity = identity
        self._conversations = dict()
        self._id_keys = dict()

    def _determine_conversation_key(self, screen_name=None, tweet_id=None, inbox_item=None, outbox_item=None):
        if screen_name and tweet_id:
            if tweet_id in self._id_keys:
                return self._id_keys[tweet_id]
            else:
                key = "{} {}".format(screen_name, tweet_id)
                self._id_keys[tweet_id] = key
                return key

        elif inbox_item:

            # todo,  favourites, events esp favourited, DM's
            if inbox_item.is_tweet:

                if inbox_item.in_reply_to_id_str and inbox_item.in_reply_to_id_str in self._id_keys:
                    # replied
                    return self._id_keys[inbox_item.in_reply_to_id_str]
                elif inbox_item.quoted_status_id_str and inbox_item.quoted_status_id_str in self._id_keys:
                    # quoted
                    return self._id_keys[inbox_item.quoted_status_id_str]
                elif inbox_item.in_reply_to_id_str and inbox_item.in_reply_to_id_str in self._id_keys:
                    # retweeted
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
                # todo retweet/quote
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
            return conversation

    def outgoing(self, outbox_item):
        conversation_key = self._determine_conversation_key(outbox_item=outbox_item)
        if conversation_key:
            if conversation_key not in self._conversations:
                self._conversations[conversation_key] = Conversation(conversation_key=conversation_key)
            conversation = self._conversations[conversation_key]
            conversation.outgoing(identity=self._identity, outbox_item=outbox_item)
            return conversation

    def housekeep(self):
        limit = datetime.datetime.now() + datetime.timedelta(hours=-1)
        delete_us = list([k for k, v in self._conversations.items() if v.last_updated() and v.last_updated() < limit])
        if delete_us:
            logger.info("removing {} conversations ".format(len(delete_us)))
            for k in delete_us:
                self._conversations.pop(k, None)
        logger.info("tracking {} conversations".format(len(self._conversations)))

    def track_replies(self, tweet_id, response):
        conversation_key = self._determine_conversation_key(
            screen_name=self._identity.screen_name,
            tweet_id=tweet_id)
        if conversation_key:
            self._conversations[conversation_key].add_response(response=response)
