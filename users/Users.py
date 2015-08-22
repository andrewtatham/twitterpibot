
from User import User
import pickle
import os
from MyTwitter import MyTwitter
import logging
from UserList import UserList
from multiprocessing import Lock
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
        self.lock = Lock()

        self._users = {}
        self._lists = {}

        exists = os.path.isfile("USERS.pkl") and os.path.isfile("USER_LISTS.pkl")
        if (exists):
            self._users = pickle.load(open("USERS.pkl", "rb"))
            self._lists = pickle.load(open("USER_LISTS.pkl", "rb"))

    def updateLists(args):
        with args.lock:
            print("updating user lists")
            logging.info("updating user lists")
            with MyTwitter() as twitter:
                myLists = twitter.show_owned_lists()
                for myList in myLists["lists"]:
                    text = "updating user list " + myList["id_str"] + " " + myList["name"]
                    print(text)
                    logging.info(text)
                    members = twitter.get_list_members(list_id = myList["id_str"])


                    key = myList["id_str"]
                
                    if not args._lists.has_key(key):
                        args._lists[key] = UserList(myList["name"])
                    args._lists[key].UpdateMembers(members)


    def getUser(args, id):
        with args.lock:
            if not args._users.has_key(id):
                args._users[id] = User(id = id)

            if(args._users[id].isStale()):
                args._users[id].update(args._lists)

            return args._users[id]

    def Save(args):
        with args.lock:
            if any(args._users) and any(args._lists):
                pickle.dump(args._users, open("USERS.pkl", "wb"))
                pickle.dump(args._lists, open("USER_LISTS.pkl", "wb"))
        
