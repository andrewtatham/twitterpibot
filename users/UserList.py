class UserList(object):
    def __init__(self, listData, membersData, *args, **kwargs):
        self.name = listData["name"] 

        self._members = set()
        for member in membersData["users"]:
            self._members.add(member["id_str"])

    def ContainsUser(args, id):
        return id in args._members


