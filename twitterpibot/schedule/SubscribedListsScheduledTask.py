import logging
import random
import time

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class SubscribedListsScheduledTask(ScheduledTask):
    def __init__(self, master_identity):
        ScheduledTask.__init__(self, master_identity)

    def get_trigger(self):
        return IntervalTrigger(hours=5)

    def on_run(self):
        self.synchronize_subscriptions()

    def synchronize_subscriptions(self):
        master_subscriptions = self.identity.twitter.get_list_subscriptions()
        master_subs_id_list = list(map(lambda sub: sub["id_str"], master_subscriptions["lists"]))

        if self.identity.slave_identities:
            for identity in self.identity.slave_identities:
                slave_subscriptions = identity.twitter.get_list_subscriptions()
                slave_subs_id_set = set(map(lambda sub: sub["id_str"], slave_subscriptions["lists"]))
                for master_sub_id in master_subs_id_list:
                    if master_sub_id not in slave_subs_id_set:
                        logger.info("Subscribing to list id %s" % master_sub_id)
                        identity.twitter.subscribe_to_list(master_sub_id)
                        time.sleep(random.randint(1, 3))
