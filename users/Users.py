
from User import User
import pickle
import os
class Users(object):
    def __init__(self, *args, **kwargs):
        self.me ={
            "name":"andrewtathampi",
            "id":"2935295111"
        }

        self.ppl = [
            {
                "name":"andrewtatham", 
                "id": "19201332"
            }
        ]

        self._users = {}
        self._lists = []

        exists = os.path.isfile("USERS.pkl") and os.path.isfile("USER_LISTS.pkl")
        if (exists):
            self._users = pickle.load(open("USERS.pkl", "rb"))
            self._lists = pickle.load(open("USER_LISTS.pkl", "rb"))

    def updateLists(args, lists):
        args._lists = lists

    def getUser(args, id):
        if not args._users.has_key(id):
            args._users[id] = User(id = id)

        if(args._users[id].isStale()):
            args._users[id].update(lists = args._lists)

        return args._users[id]

    def Save(args):
        if any(args._users) and any(args._lists):
            pickle.dump(args._users, open("USERS.pkl", "wb"))
            pickle.dump(args._lists, open("USER_LISTS.pkl", "wb"))
        
