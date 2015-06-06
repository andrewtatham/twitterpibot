try:    
    from piglow import PiGlow
except Exception:
    enablePiglow = False


def PiglowTasks():
    piglow = None
    if enablePiglow:
        piglow = PiGlow()
        maxbright = 32
        piglow.all(0)
        pattern = [[0 for x in range(360)]for y in range(18)]
        for t in range(360):
            for colour in range(6):
                for arm in range(3):
                    b1 = math.sin(math.radians(t + arm * 15 + colour * 360 / 32))
                    led = getLed(arm,colour)
                    pattern[led][t] = getBright(b1)

        while running and enablePiglow:
            try:
                for t in range(360):
                    for led in range(18):
                        piglow.led(led + 1, pattern[led][t])
                    if running:
                        sleep(1) 
                    else:
                        break
            except Exception as e:
                logging.exception(e.message, e.args)             
                pprint.pprint(e)


def getLed(arm,colour):
    return int(6 * arm + colour)
def getBright(factor):
    return max(0, min(int(-0.5 * maxbright + maxbright * factor),255))

