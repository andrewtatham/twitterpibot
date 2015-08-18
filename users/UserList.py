class UserList(object):
    def __init__(self, list, members, *args, **kwargs):
        self.name = list["name"] 

        self.members = set()
        for member in members["users"]:
            self.members.add(member["id_str"])



