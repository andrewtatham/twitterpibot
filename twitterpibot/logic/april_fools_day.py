import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.logic import conversation
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

_items = [
    "an ac battery",
    "a pint of ants' milk",
    "a runaround",
    "a bubble for a spirit level",
    "a bucket of steam",
    "a bucket of compressed air",
    "a can of blue steam",
    "a copper magnet",
    "a litre of dry water",
    "a tin of elbow grease",
    "a flux capacitor",
    "a glass axe",
    "a glass hammer",
    "a glass magnet",
    "a pint of gnat's milk",
    "a grape grater",
    "a hard punch",
    "a dozen holes for the hole puncher",
    "six horizontal tentpegs",
    "a left-handed box-end wrench",
    "a left-handed gavel",
    "a left-handed monkey wrench",
    "a left-handed paint roller",
    "a left-handed punch",
    "a right-handed punch",
    "a left handed screwdriver",
    "a left-handed tablespoon",
    "a liquid magnet",
    "a long drop",
    "a long stand",
    "a long weight",
    "sixteen mercury rods",
    "some non-conductive cardboard",
    "a metric adjustable spanner",
    "a imperial adjustable spanner",
    "a glass hammer",
    "a left handed screw driver",
    "a skirtingboard ladders",
    "a dozen sky hooks",
    "some spirit level bubbles",
    "a reversable drill to fill holes back in",
    "a box of rubber nails",
    "a long weight",
    "a box of left handed screws",
    "a tin of elbow grease",
    "a bag of pixels for a monitor",
    "a bucket of 3/4 inch holes",
    "a box of 16mm valve clearances",
    "a bucket of metal sparks",
    "a length of pachyderm trunking",
    "a can of polka-dot paint",
    "a dozen ring centres",
    "a roll of film for the digital camera,",
    "two siren winders",
    "a packet of skyhooks",
    "a bottle of snake oil",
    "a socket for round nuts",
    "half a pound of electricity",
    "a kilo of internet",
    "a tub of sonar grease",
    "sparks for the fire",
    "sparks for the grinder",
    "spark samples from the angle grinder",
    "a can of striped paint",
    "a tin of tartan paint",
    "a ball of tartan wool",
    "a tuning pipe for a fog horn",
    "a lost document file",
    "some virtual ram for the server",
    "a virtual machine",
    "a water hammer",
    "some white ink for the printer",
    "winter grade air for winter tyres",
    "a wiremesh watering can",
    "a yard of shoreline",
]


class AprilFoolsDayScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(AprilFoolsDayScheduledTask, self).__init__(identity)
        self._list = []

    def get_trigger(self):
        return CronTrigger(month=4, day=1, hour="0-11", minute=random.randint(0, 59))

    def _item(self):
        if not self._list:
            self._list = list(_items)
            random.shuffle(self._list)
        item = self._list.pop()
        return item

    def on_run(self):
        text = self.get_shopping_list()
        self.identity.twitter.send(OutgoingTweet(text=text))

    def get_shopping_list(self):
        text = random.choice(conversation.hello_words)
        text += " @andrewtatham sent me to buy "
        text += self._item()
        text += " and "
        text += self._item()
        if random.randint(0, 1):
            text += ". Do you have any?"
        else:
            text += ". Can you help?"
        return text


if __name__ == '__main__':
    import main

    identity = main.AndrewTathamPiIdentity(None)
    task = AprilFoolsDayScheduledTask(identity)
    for i in range(100):
        text = task.get_shopping_list()
        print(len(text), text)
