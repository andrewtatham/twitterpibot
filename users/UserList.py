class UserList(object):
    def __init__(self, list, members, *args, **kwargs):

        # 217465147 Retweet Less
        # 217465126 Retweet More
        # 217465004 Awesome Bots

        self.name = list["name"] 

        self.members = set()
        for member in members["users"]:
            self.members.add(member["id_str"])



