
from User import User
import pickle
import os
from MyTwitter import MyTwitter
import logging
from UserSet import UserSet
import threading
class Users(object):
    def __init__(self, *args, **kwargs):
        self.me = {
            "name":"andrewtathampi",
            "id":"2935295111"
        }

        self.ppl = [{
                "name":"andrewtatham", 
                "id": "19201332"
            }]
        self.lock = threading.Lock()

        self._users = {}
        self._sets = {}

        #exists = os.path.isfile("USERS.pkl") and
        #os.path.isfile("USER_LISTS.pkl")
        #if (exists):
        #    self._users = pickle.load(open("USERS.pkl", "rb"))
        #    self._sets = pickle.load(open("USER_LISTS.pkl", "rb"))

    def updateLists(args):
        #print("updating user lists")
        #logging.info("updating user lists")
        with MyTwitter() as twitter:
            myLists = twitter.show_owned_lists()
            for myList in myLists["lists"]:
                #text = "updating user list " + myList["id_str"] + " " + myList["name"]
                #print(text)
                #logging.info(text)
                members = twitter.get_list_members(list_id = myList["id_str"])
                key = myList["id_str"]
                with args.lock:
                    if not args._sets.has_key(key):
                        args._sets[key] = UserSet(myList["name"])
                    set = args._sets[key]
                    set.UpdateMembers(members)


    def getUser(args, id = None, data = None):
        if not id and not data:
            raise ValueError()

        with args.lock:

            if id and not data:
                with MyTwitter() as twitter:
                    data = twitter.lookup_user(user_id = id)[0]

            if data:
                id = data["id_str"]

                if not args._users.has_key(id):
                    args._users[id] = User(data)

                if(args._users[id].isStale()):
                    args._users[id].update(args._sets)

                return args._users[id]



