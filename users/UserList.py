class UserList(object):
    def __init__(self, list, members, *args, **kwargs):
        self.name = list["name"] 

        self._members = set()
        for member in members["users"]:
            self._members.add(member["id_str"])

    def ContainsUser(args, id):
        return id in args._members


