import datetime
import pprint


def parse_int(param):
    if param:
        return int(param)
    else:
        return 0


class User(object):
    def __init__(self, data, my_screen_name):

        self.id_str = data.get("id_str")
        self.name = data.get("name")
        self.screen_name = data.get("screen_name")
        self.description = data.get("description")
        self.url = data.get("url")
        self.profile_image_url = data.get("profile_image_url")
        self.profile_banner_url = data.get("profile_banner_url")
        if self.profile_banner_url:
            self.profile_banner_url += "/300x100"

        self.is_me = bool(self.screen_name == my_screen_name)

        self.following = bool(data.get("following"))
        self.verified = bool(data.get("verified"))
        self.location = data.get("location")
        self.protected = bool(data.get("protected"))

        self.friends_count = parse_int(data.get("friends_count"))
        self.followers_count = parse_int(data.get("followers_count"))
        self.statuses_count = parse_int(data.get("statuses_count"))

        self.updated = None

        self.is_arsehole = False
        self.is_do_not_retweet = False
        self.is_retweet_more = False
        self.is_awesome_bot = False
        self.is_friend = False
        self.is_reply_less = False

        self.is_possibly_bot = self.screen_name and "bot" in self.screen_name.lower() \
                               or self.name and "bot" in self.name.lower() \
                               or self.description and "bot" in self.description.lower()

    def is_stale(self):
        if self.updated:
            delta = datetime.datetime.utcnow() - self.updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            return mins > 45
        else:
            return True

    def __str__(self):
        return self.name + " [@" + self.screen_name + "] (" + str(self.description) + ")"


if __name__ == '__main__':
    import main

    identity = main.AndrewTathamPiIdentity(None)
    members = identity.twitter.get_list_members(identity.lists._list_ids["Awesome Bots"])["users"]
    pprint.pprint(members)
    members = list(map(lambda member: User(member, identity.screen_name), members))

    for member in members:
        print(member)
