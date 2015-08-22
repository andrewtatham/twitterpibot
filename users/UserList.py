from multiprocessing import Lock
class UserList(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.lock = Lock()
        self._members = set()

    def ContainsUser(args, id):
        with args.lock:
            return id in args._members

    def UpdateMembers(args, membersData):
        newMembers = set()
        for member in membersData["users"]:
            id = member["id_str"]
            newMembers.add(id)
        with args.lock:
            args._members = newMembers
