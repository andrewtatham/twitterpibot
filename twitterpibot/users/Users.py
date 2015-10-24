from User import User
from twitterpibot.twitter.MyTwitter import MyTwitter

import threading
from twitterpibot.users.UserSet import UserSet

_lock = threading.Lock()
_users = {}
_sets = {}


def updateLists():
    with MyTwitter() as twitter:
        myLists = twitter.show_owned_lists()
        for myList in myLists["lists"]:
            members = twitter.get_list_members(list_id=myList["id_str"])
            key = myList["id_str"]
            with _lock:
                if key not in _sets:
                    _sets[key] = UserSet(myList["name"])
                set = _sets[key]
                set.UpdateMembers(members)


def getUser(id=None, data=None):
    if not id and not data:
        raise ValueError()

    with _lock:

        if id and not data:
            with MyTwitter() as twitter:
                data = twitter.lookup_user(user_id=id)[0]

        if data:
            id = data["id_str"]

            if id not in _users:
                _users[id] = User(data)

            if _users[id].isStale():
                _users[id].update(_sets)

            return _users[id]
