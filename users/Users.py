
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

        self.users = {}
        self.lists = []

        exists = os.path.isfile("USERS.pkl") and os.path.isfile("USER_LISTS.pkl")
        if (exists):
            self.users = pickle.load(open("USERS.pkl", "rb"))
            self.lists = pickle.load(open("USER_LISTS.pkl", "rb"))
    

    def getUser(args, id):



        if not args.users.has_key(id):
            args.users[id] = User(id)

        if(args.users[id].isStale()):
            args.users[id].update(args.lists)


        return args.users[id]


    def Save(args):
        if any(args.users) and any(args.lists):
            pickle.dump(args.users, open("USERS.pkl", "wb"))
            pickle.dump(args.lists, open("USER_LISTS.pkl", "wb"))
        
