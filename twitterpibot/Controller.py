import random

import twitterpibot.identities

__author__ = 'andrewtatham'


def get_user_dto(user):
    return {
        "user_id": user.id,
        "name": user.name,
        "screen_name": user.screen_name,
        "description": user.description,
        "url": user.url,
        "profile_image_url": user.profile_image_url,
        "profile_banner_url": user.profile_banner_url

    }


def get_action_dto(label, url):
    return {
        "label": label,
        "url": url
    }


def get_identities_dto(identity):
    dto = {
        "screen_name": identity.screen_name,
        "id_str": identity.id_str,
        "url": "identity/" + identity.screen_name
    }
    return dto


def get_identity_dto(identity):
    dto = get_identities_dto(identity)
    if identity.following:
        dto["following"] = [{"follower_id": f} for f in identity.following]
    if identity.lists:
        dto["lists"] = [
            {
                "list_name": l,
                "members": [
                    {
                        "list_member_id": list_member_id
                    } for list_member_id in identity.lists._sets[l]]
            } for l in identity.lists._sets]
    if identity.users:
        dto["users"] = [get_user_dto(user)
                        for user_id, user in identity.users._users.items()]
    return dto


class Controller(object):
    def get_identities(self):
        return [get_identities_dto(i) for i in twitterpibot.identities.all_identities]

    def get_identity(self, screen_name=None):
        return [get_identity_dto(i) for i in twitterpibot.identities.all_identities
                if screen_name == i.screen_name][0]

    def get_actions(self):
        return [get_action_dto(a[0], a[1]) for a in [
            ("home", "/"),
            ("demo", "/demo"),
            ("init", "/init"),
            ("actions", "/actions"),
            ("identities", "/identities"),
            ("following", "/following"),
            ("followinggraph", "/followinggraph"),
            ("shutdown", "/shutdown")
        ]]

    def get_following(self):
        dto = []
        for identity in twitterpibot.identities.all_identities:
            if identity.following:
                for following in identity.following:
                    dto.append((identity.id_str, following))

        return dto

    def get_following_graph(self):
        nodes = {}
        edges = {}
        for identity in twitterpibot.identities.all_identities:

            nodes[identity.id_str] = \
                {
                    "id_str": identity.id_str,
                    "screen_name": identity.screen_name
                }
            edges[identity.id_str] = {}
            if identity.following:
                random.shuffle(identity.following)
                for following in identity.following[:10]:
                    node = {
                        "id_str": following
                    }
                    user = identity.users.get_user(user_id=following)
                    if user:
                        node["screen_name"] = user.screen_name

                    nodes[following] = node
                    edge = {}
                    edges[identity.id_str][following] = edge

        dto = {
            "nodes": nodes,
            "edges": edges
        }
        return dto
