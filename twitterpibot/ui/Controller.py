from twitterpibot import identities

__author__ = 'andrewtatham'


class Controller(object):
    def get_identities(self, screen_name=None):
        return [self.get_identity_model(i) for i in identities.all_identities
                if screen_name is None or screen_name == i.screen_name]

    def get_actions(self):
        return [self.get_action_model(a[0], a[1]) for a in [
            ("home", "/"),
            ("init", "/init"),
            ("identity", "/identity"),
            ("shutdown", "/shutdown")
        ]]

    def get_identity_model(self, identity):
        return {
            "screen_name": identity.screen_name,
            "url": "identity/" + identity.screen_name
        }

    def get_action_model(self, label, url):
        return {
            "label": label,
            "url": url
        }
