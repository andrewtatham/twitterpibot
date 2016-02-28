from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask


class FollowScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=4)

    def on_run(self):
        list_names = ["Awesome Bots", "Retweet More"]
        for list_name in list_names:
            if list_name in self.identity.lists._sets:
                list_members = self.identity.lists._sets[list_name]
                if list_members and self.identity.following:
                    unfollowed = list(list_members.difference(self.identity.following))
                    if unfollowed:
                        for user_id in unfollowed[:1]:
                            self.identity.twitter.follow(user_id=user_id)
                            self.identity.following.add(user_id)
