import random

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
