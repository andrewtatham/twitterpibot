import logging
import random
import time

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class SubscribedListsScheduledTask(ScheduledTask):
    def __init__(self, identity, master_identity):
        super(SubscribedListsScheduledTask, self).__init__(identity)
        self._master_identity = master_identity

    def get_trigger(self):
        return IntervalTrigger(minutes=57)

    def on_run(self):
        self.synchronize_subscriptions()

    def synchronize_subscriptions(self):
        master_subscriptions = self._master_identity.twitter.get_list_subscriptions()
        master_subs_id_list = set(map(lambda sub: sub["id_str"], master_subscriptions["lists"]))

        slave_subscriptions = self.identity.twitter.get_list_subscriptions()
        slave_subs_id_set = set(map(lambda sub: sub["id_str"], slave_subscriptions["lists"]))

        subscribe_to_list_ids = master_subs_id_list.difference(slave_subs_id_set)
        if subscribe_to_list_ids:
            for subscribe_to_list_id in subscribe_to_list_ids:
                logger.info("Subscribing to list id %s" % subscribe_to_list_id)
                self.identity.twitter.subscribe_to_list(subscribe_to_list_id)
                time.sleep(random.randint(1, 3))
