import random

import re

from twitterpibot.webserver import shutdown
from twitterpibot.data_access import dal
from twitterpibot.logic.conversation import hello_words, thanks_and_bye
from twitterpibot.responses.Response import Response


class RestartResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "restart" in inbox_item.text

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(inbox_item, text=random.choice(hello_words) + " restarting...")
        shutdown()
        self.identity.twitter.reply_with(inbox_item, text="...restarting. " + random.choice(thanks_and_bye))


class ImportTokensResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "import tokens" in inbox_item.text

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(inbox_item, text=random.choice(hello_words) + " importing...")
        dal.import_tokens("tokens.csv")
        self.identity.twitter.reply_with(inbox_item, text="...importing done. " + random.choice(thanks_and_bye))


class ExportTokensResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "export tokens" in inbox_item.text

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(inbox_item, text=random.choice(hello_words) + " exporting...")
        dal.export_tokens("tokens.csv")
        self.identity.twitter.reply_with(inbox_item, text="...exporting done. " + random.choice(thanks_and_bye))


set_token_rx = re.compile("^set token (?P<key>[\w\s]+) = (?P<value>[\w\s]+)$")


class SetTokenResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "set token" in inbox_item.text and set_token_rx.match(inbox_item.text)

    def respond(self, inbox_item):
        key, value = self.parse(inbox_item.text)
        if key and value:
            before_text = "{} setting {} to {}".format(random.choice(hello_words), key, value)
            self.identity.twitter.reply_with(inbox_item, text=before_text)
            dal.set_token(key, value)
            self.identity.twitter.reply_with(inbox_item, text="...done. " + random.choice(thanks_and_bye))

    @staticmethod
    def parse(text):
        match = set_token_rx.match(text)
        if match:
            key = match.group("key")
            value = match.group("value")
            return key, value


class DropCreateTablesResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "drop create" in inbox_item.text

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(
            inbox_item,
            text=random.choice(hello_words) + " dropping & creating...")
        dal.drop_create_tables()
        self.identity.twitter.reply_with(
            inbox_item,
            text="...dropping & creating done. " + random.choice(thanks_and_bye))
