import twitterpibot.identities

__author__ = 'andrewtatham'


class Controller(object):
    def get_identities(self, screen_name=None):
        # for identity in twitterpibot.identities.all_identities:
        #     pprint.pprint(identity.__dict__)
        #     pprint.pprint(identity.lists._list_names)
        #     pprint.pprint(identity.lists._list_ids)
        #     pprint.pprint(identity.lists._sets)
        #     pprint.pprint(identity.users._users)

        return [self.get_identity_dto(i) for i in twitterpibot.identities.all_identities
                if screen_name is None or screen_name == i.screen_name]

    def get_actions(self):
        return [self.get_action_dto(a[0], a[1]) for a in [
            ("home", "/"),
            ("init", "/init"),
            ("identity", "/identity"),
            ("shutdown", "/shutdown")
        ]]

    def get_identity_dto(self, identity):
        dto = {
            "screen_name": identity.screen_name,
            "url": "identity/" + identity.screen_name
        }
        if identity.following:
            dto["following"] = [{"follower_id": f} for f in identity.following]
        if identity.lists:
            dto["lists"] = [{"list_name": l} for l in identity.lists._sets]
        if identity.users:
            dto["users"] = [{"user_id": u} for u in identity.users._users]
        return dto

    def get_action_dto(self, label, url):
        return {
            "label": label,
            "url": url
        }
