import colorama

from identity import BotIdentity


class ScrollBotIdentity(BotIdentity):
    def __init__(self, admin_identity=None):
        super(ScrollBotIdentity, self).__init__(
            screen_name="scroll_bot",
            id_str="863364063316893696",
            admin_identity=admin_identity)
        self.colour = colorama.Fore.YELLOW