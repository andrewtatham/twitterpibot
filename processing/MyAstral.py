from astral import Astral
import datetime
class MyAstral(object):
    def GetTimes(args):
                
        astral = Astral()
        city = astral['Leeds']
        sun = city.sun(date=datetime.date.today(), local = True)

        print("[Astral] dawn: " + str(sun['dawn']))
        print("[Astral] sunrise: " + str(sun['sunrise']))
        print("[Astral] noon: " + str(sun['noon']))
        print("[Astral] sunset: " + str(sun['sunset']))
        print("[Astral] dusk: " + str(sun['dusk']))
        return sun

    def GetTommorrowTimes(args):
                
        astral = Astral()
        city = astral['Leeds']
        sun = city.sun(date=datetime.date.today() + datetime.timedelta(days = 1) , local = True)

        print("[Astral] dawn: " + str(sun['dawn']))
        print("[Astral] sunrise: " + str(sun['sunrise']))
        print("[Astral] noon: " + str(sun['noon']))
        print("[Astral] sunset: " + str(sun['sunset']))
        print("[Astral] dusk: " + str(sun['dusk']))

        return sun