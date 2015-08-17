
from User import User
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


    

    def getUser(args, id):

        if not args.users.has_key(id):
            args.users[id] = User(id, args.lists)

        return args.users[id]


        
