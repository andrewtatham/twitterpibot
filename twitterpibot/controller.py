import pprint
from itertools import groupby
from operator import attrgetter
import random

import logging
from twitterpibot.data_access import dal

__author__ = 'andrewtatham'
logger = logging.getLogger(__name__)
_identities_list = []
_identities_dic = {}


def set_identities(identities):
    global _identities_list
    global _identities_dic
    _identities_list = identities
    _identities_dic = dict(map(lambda i: (i.id_str, i), identities))


def get_tweet_dto(tweet):
    tweet_dto = {
        "text": tweet.text
    }
    return tweet_dto


def get_user_dto(user):
    user_dto = {
        "user_id": user.id_str,
        "name": user.name,
        "screen_name": user.screen_name,
        "description": user.description,
        "flags": user.flags,
        "url": user.url,
        "profile_image_url": user.profile_image_url,
        "profile_banner_url": user.profile_banner_url,
        "location": user.location,
        "profile_url": user.profile_url,
        "last_tweeted_at": user.last_tweeted_at,
        "last_tweeted": user.get_last_tweeted(),

    }
    if user._latest_tweets:
        user_dto["latest_tweets"] = list(map(get_tweet_dto, user._latest_tweets))
    if user._user_score:
        user_dto["score"] = user._user_score._scores
    # todo availiable actions e.g. can follow, unfollow, block, report etc - enable/disable buttons
    return user_dto


def _filter_users(users):
    return list(filter(lambda u: u._user_score, users))


def _sort_users(users):
    users.sort(key=lambda u: u._user_score._scores["total"])
    return users


def _map_users(users):
    return list(map(get_user_dto, users))


def get_users_dto(users):
    following = set(users.get_following())
    followers = set(users.get_followers())
    all = set(users._users.keys())

    following_followers = users.get_users(following.intersection(followers), lookup=False)
    following_only = users.get_users(following.difference(followers), lookup=False)
    followers_only = users.get_users(followers.difference(following), lookup=False)
    others = users.get_users(all.difference(following.union(followers)), lookup=False)

    following_followers = _map_users(_sort_users(_filter_users(following_followers)))
    following_only = _map_users(_sort_users(_filter_users(following_only)))
    followers_only = _map_users(_sort_users(_filter_users(followers_only)))
    others = _map_users(_sort_users(_filter_users(others)))

    dto = {
        "following_followers": following_followers,
        "following_only": following_only,
        "followers_only": followers_only,
        "others": others,
    }

    return dto


def get_action_dto(label, url):
    return {
        "label": label,
        "url": url
    }


def get_identities_dto(identity):
    dto = {
        "id_str": identity.id_str,
        "name": identity.name,
        "screen_name": identity.screen_name,
        "profile_image_url": identity.profile_image_url,
        "action_url": "identity/" + identity.id_str,
    }
    return dto


def get_identity_dto(identity):
    dto = {
        "id_str": identity.id_str,
        "name": identity.name,
        "screen_name": identity.screen_name,
        "description": identity.description,
        "location": identity.location,
        "url": identity.url,
        "profile_url": identity.profile_url,
        "profile_banner_url": identity.profile_banner_url,
        "profile_image_url": identity.profile_image_url,


        "following_count": identity.following_count,
        "followers_count": identity.followers_count,
        "statuses_count": identity.statuses_count,
        "favourites_count": identity.favourites_count,
    }
    # if identity.users._following:
    #     dto["following"] = [{"follower_id": f} for f in identity.users._following]
    # if identity.users._lists:
    #     dto["lists"] = [
    #         {
    #             "list_name": l,
    #             "members": [
    #                 {
    #                     "list_member_id": list_member_id
    #                 } for list_member_id in identity.users._lists._sets[l]]
    #         } for l in identity.users._lists._sets]
    if identity.users:
        dto["users"] = get_users_dto(identity.users)
    return dto


def get_identities():
    return [get_identities_dto(i) for i in _identities_list]


def get_identity(id_str):
    identity = _identities_dic.get(id_str)
    if identity:
        return get_identity_dto(identity)


def get_actions():
    actions = [
        ("home", "/"),
        ("demo", "/demo"),
        ("init", "/init"),
        ("actions", "/actions"),
        ("identities", "/identities"),
    ]
    actions.extend([("identitity @" + i.screen_name, "/identity/" + i.id_str) for i in _identities_list])

    actions.extend([
        ("following", "/following"),
        ("followinggraph", "/followinggraph"),
        ("exceptions", "/exceptions"),
        ("exceptionsummary", "/exceptionsummary"),
        ("shutdown", "/shutdown")
    ])
    return [get_action_dto(a[0], a[1]) for a in actions]


def get_following():
    dto = []
    for identity in _identities_list:
        if identity.users._following:
            for following in identity.users._following:
                dto.append((identity.id_str, following))

    return dto


def get_following_graph():
    nodes = {}
    edges = {}
    identity_ids = set()
    # add identity nodes
    for identity in _identities_list:
        identity_ids.add(identity.id_str)
        nodes[identity.id_str] = \
            {
                "screen_name": identity.screen_name,
                "profile_image_url": identity.profile_image_url,
                "mass": 10
            }
        # init identity edges
        edges[identity.id_str] = {}

        # add edges between identities
        for identity2 in _identities_list:
            if identity2.id_str in identity.users._following:
                edge_data = {"length": random.randint(50, 70)}
                edges[identity.id_str][identity2.id_str] = edge_data

    # get a list of users to add
    users_list = []
    for identity in _identities_list:
        identity_users_list = []
        for k, v in identity.users._users.items():
            identity_users_list.append(v)
        random.shuffle(identity_users_list)
        users_list.extend(identity_users_list)

    # add user nodes
    for user in users_list:
        if user.id_str not in identity_ids:
            nodes[user.id_str] = \
                {
                    "screen_name": user.screen_name,
                    "profile_image_url": user.profile_image_url
                }

            # add following edges
            for identity in _identities_list:
                if user.id_str in identity.users._following:
                    edge_data = {"length": random.randint(20, 40)}
                    edges[identity.id_str][user.id_str] = edge_data

    dto = {
        "nodes": nodes,
        "edges": edges
    }
    return dto


def get_exception_dto(exception):
    return {
        "now": exception.now,
        "uptime": exception.uptime,
        "boottime": exception.boottime,
        "screen_name": exception.screen_name,
        "label": exception.label,
        "message": exception.message,
        "stack_trace": exception.stack_trace,
    }


def get_exceptions():
    return list(map(get_exception_dto, dal.get_exceptions()))


def _get_exception_summary(exceptions_list):
    retval = []
    grouper = attrgetter("label", "message", "stack_trace")
    if exceptions_list:
        exceptions_list.sort(key=grouper)
        for key, group in groupby(exceptions_list, grouper):
            item = dict(zip(["label", "message", "stack_trace"], key))
            item['count'] = len(list(group))
            retval.append(item)
        retval.sort(key=lambda msg: msg["count"])
        retval.reverse()
    return retval


def ex_type_grouper(ex):
    return ex.log_type


date_grouper = attrgetter("now.year", "now.month", "now.day")
hour_grouper = attrgetter("now.year", "now.month", "now.day", "now.hour")
day_header = ["year", "month", "day"]
hour_header = list(day_header)
hour_header.append("hour")


def get_exception_summary():
    retval = {}
    exceptions_list = dal.get_exceptions()
    if exceptions_list:
        exceptions_list.sort(key=ex_type_grouper)
        for log_type, group in groupby(exceptions_list, ex_type_grouper):
            retval[log_type] = _get_exception_summary(list(group))
    return retval


def get_exceptions_chart_data():
    retval = []
    header = list(hour_header)
    header.extend(["exceptions", "warnings"])
    retval.append(header)
    exceptions_list = dal.get_exceptions()
    if exceptions_list:

        exceptions_list.sort(key=hour_grouper)
        for date_key, date_group in groupby(exceptions_list, hour_grouper):

            row = list(date_key)

            date_group_list = list(date_group)
            date_group_list.sort(key=ex_type_grouper)
            d = {
                "Warning": 0,
                "Excepton": 0
            }
            for type_key, type_group in groupby(date_group_list, ex_type_grouper):
                d[type_key] = len(list(type_group))
            row.append(d["Excepton"])
            row.append(d["Warning"])
            retval.append(tuple(row))
    return retval


if __name__ == '__main__':
    pprint.pprint(get_exceptions())
    pprint.pprint(get_exception_summary())
    pprint.pprint(get_exceptions_chart_data())


def follow(identity_id, user_id):
    if identity_id in _identities_dic:
        logger.info("following user id {}".format(user_id))
        _identities_dic[identity_id].users.follow(user_id)


def unfollow(identity_id, user_id):
    if identity_id in _identities_dic:
        logger.info("unfollowing user id {}".format(user_id))
        _identities_dic[identity_id].users.unfollow(user_id)


def block(identity_id, user_id):
    if identity_id in _identities_dic:
        logger.info("blocking user id {}".format(user_id))
        _identities_dic[identity_id].users.block(user_id)


def report(identity_id, user_id):
    if identity_id in _identities_dic:
        logger.info("reporting user id {}".format(user_id))
        _identities_dic[identity_id].users.report(user_id)
