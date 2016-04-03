from twitterpibot.bootstrap import shutdown
from twitterpibot.data_access import dal

from twitterpibot.responses.Response import Response


class RestartResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "restart" in inbox_item.text

    def respond(self, inbox_item):
        shutdown()


class ImportTokensResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "import tokens" in inbox_item.text

    def respond(self, inbox_item):
        dal.import_tokens("tokens.csv")


class ExportTokensResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "export tokens" in inbox_item.text

    def respond(self, inbox_item):
        dal.export_tokens("tokens.csv")


class DropCreateTablesResponse(Response):
    def condition(self, inbox_item):
        return inbox_item.is_direct_message and inbox_item.sender.screen_name == self.identity.admin_screen_name \
               and "drop create" in inbox_item.text

    def respond(self, inbox_item):
        dal.drop_create_tables()
