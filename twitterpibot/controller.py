from itertools import groupby
from operator import attrgetter
import random

import twitterpibot
import twitterpibot.bootstrap
from twitterpibot.data_access import dal

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
    if identity.users.following:
        dto["following"] = [{"follower_id": f} for f in identity.users.following]
    if identity.users.lists:
        dto["lists"] = [
            {
                "list_name": l,
                "members": [
                    {
                        "list_member_id": list_member_id
                    } for list_member_id in identity.users.lists._sets[l]]
            } for l in identity.users.lists._sets]
    if identity.users:
        dto["users"] = [get_user_dto(user)
                        for user_id, user in identity.users._users.items()]
    return dto


def get_identities():
    return [get_identities_dto(i) for i in twitterpibot.bootstrap.all_identities]


def get_identity(screen_name=None):
    return [get_identity_dto(i) for i in twitterpibot.bootstrap.all_identities
            if screen_name == i.screen_name][0]


def get_actions():
    return [get_action_dto(a[0], a[1]) for a in [
        ("home", "/"),
        ("demo", "/demo"),
        ("init", "/init"),
        ("actions", "/actions"),
        ("identities", "/identities"),
        ("following", "/following"),
        ("followinggraph", "/followinggraph"),
        ("exceptions", "/exceptions"),
        ("exceptionsummary", "/exceptionsummary"),
        ("shutdown", "/shutdown")
    ]]


def get_following():
    dto = []
    for identity in twitterpibot.bootstrap.all_identities:
        if identity.users.following:
            for following in identity.users.following:
                dto.append((identity.id_str, following))

    return dto


def get_following_graph():
    nodes = {}
    edges = {}
    identity_ids = set()
    # add identity nodes
    for identity in twitterpibot.bootstrap.all_identities:
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
        for identity2 in twitterpibot.bootstrap.all_identities:
            if identity2.id_str in identity.users.following:
                edge_data = {"length": random.randint(50, 70)}
                edges[identity.id_str][identity2.id_str] = edge_data


    # get a list of users to add
    users_list = []
    for identity in twitterpibot.bootstrap.all_identities:
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
            for identity in twitterpibot.bootstrap.all_identities:
                if user.id_str in identity.users.following:
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
            print(date_key)
            row = list(date_key)

            date_group_list = list(date_group)
            date_group_list.sort(key=ex_type_grouper)
            d = {
                "Warning": 0,
                "Excepton": 0
            }
            for type_key, type_group in groupby(date_group_list, ex_type_grouper):
                print(type_key)
                d[type_key] = len(list(type_group))
            row.append(d["Excepton"])
            row.append(d["Warning"])
            retval.append(tuple(row))
    return retval


if __name__ == '__main__':
    print(get_exceptions_chart_data())
