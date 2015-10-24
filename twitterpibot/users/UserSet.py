import threading


class UserSet(object):
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self._members = set()

    def ContainsUser(self, id):
        with self.lock:
            return id in self._members

    def UpdateMembers(self, membersData):
        newMembers = set()
        for member in membersData["users"]:
            id = member["id_str"]
            newMembers.add(id)
        with self.lock:
            self._members = newMembers
