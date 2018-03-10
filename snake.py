

import twitterpibot.hardware.unicorn.myunicornhat as uh
import twitterpibot.hardware.myhardware
import random

if __name__ == '__main__':

    uh.lights()
    for i in range(500):
        print(i)

        uh.fade()
        uh.lights()
        if i % 15 == 0 or random.randint(0, 3) == 0:
            uh.inbox_item_received(None)
        if i % 50 == 0:
            uh.on_lights_scheduled_task()

    uh.close()
    if not twitterpibot.hardware.myhardware.is_linux:
        uh.unicornhat.display()
