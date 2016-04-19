import datetime
import os

import re


def parse_int(param):
    if param:
        return int(param)
    else:
        return 0


bot_rx = re.compile("bot|ebooks|#botALLY", re.IGNORECASE)


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

        self.is_possibly_bot = self.screen_name and bot_rx.search(self.screen_name) \
                               or self.name and bot_rx.search(self.name) \
                               or self.description and bot_rx.search(self.description)
        self.flags = ""

        if self.following: self.flags += " F"
        if self.verified : self.flags += " V"
        if self.protected: self.flags += " P"

        if self.is_arsehole: self.flags += " AH"
        if self.is_friend: self.flags += " FR"
        if self.is_awesome_bot: self.flags += " AB"
        if self.is_possibly_bot: self.flags += " PB"
        if self.is_retweet_more: self.flags += " RT+"
        if self.is_do_not_retweet: self.flags += " RT-"
        if self.is_reply_less: self.flags += " RP-"
        self.flags = self.flags.strip()

    def is_stale(self):
        if self.updated:
            # noinspection PyTypeChecker
            delta = datetime.datetime.utcnow() - self.updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            return mins > 45
        else:
            return True

    def __str__(self):
        return "@{} {}".format(
            self.screen_name,
            self.flags
        )

    def short_description(self):
        return "{} [@{}] {}".format(
            self.name,
            self.screen_name,
            self.flags,

        )

    def long_description(self):
        text = self.short_description()
        if self.description:
            text += " \"" + self.description.replace(os.linesep, " ") + "\""
        if self.location:
            text += " {" + self.location + "}"
        return text


if __name__ == '__main__':
    import identities
    identity = identities.AndrewTathamPiIdentity(None)
    members = identity.twitter.get_list_members(identity.lists._list_ids["Awesome Bots"])["users"]
    # pprint.pprint(members)
    members = list(map(lambda member: User(member, identity.screen_name), members))
    i = 0
    for member in members:
        print(str(i) + " " + str(member) + os.linesep
              + member.short_description() + os.linesep
              + member.long_description())
        i += 1
