from twitterpibot import loggingconfig

loggingconfig.init()

if __name__ == '__main__':
    from twitterpibot.logic import fsh
    from twitterpibot.data_access import dal

    # dal.import_tokens(fsh.root + "tokens.csv")
    dal.export_tokens(fsh.root + "tokens.csv")

if __name__ == "__main__":

    from identities_pis import AndrewTathamPiIdentity, AndrewTathamPi2Identity, \
        NumberwangHostIdentity, \
        JulieNumberwangIdentity, SimonNumberwangIdentity, EggPunBotIdentity, WhenIsInternationalMensDayBotIdentity, \
        BotgleArtistIdentity, TheMachinesCodeIdentity
    from identities import AndrewTathamIdentity

    andrewtatham = AndrewTathamIdentity(stream=True)
    andrewtathampi = AndrewTathamPiIdentity(andrewtatham)
    andrewtathampi2 = AndrewTathamPi2Identity(andrewtatham)
    numberwang_host = NumberwangHostIdentity(andrewtatham)
    julienumberwang = JulieNumberwangIdentity(andrewtatham)
    simonnumberwang = SimonNumberwangIdentity(andrewtatham)
    eggpunbot = EggPunBotIdentity(andrewtatham)
    whenmensday = WhenIsInternationalMensDayBotIdentity(andrewtatham)
    botgleartist = BotgleArtistIdentity(andrewtatham)
    themachinescode = TheMachinesCodeIdentity(andrewtatham)

    andrewtatham.buddies = [
        andrewtathampi, andrewtathampi2,
        numberwang_host, julienumberwang, simonnumberwang,
        eggpunbot,
        whenmensday,
        botgleartist,
        themachinescode
    ]
    andrewtathampi.converse_with = andrewtathampi2
    andrewtathampi2.converse_with = andrewtathampi

    numberwang_host.contestant_pairs = [
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [julienumberwang, simonnumberwang],
        [andrewtathampi, andrewtathampi2],
    ]

    import twitterpibot.hardware.myhardware

    if twitterpibot.hardware.myhardware.is_raspberry_pi_2:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            numberwang_host,
            julienumberwang,
            simonnumberwang,
            eggpunbot,
            whenmensday,
            botgleartist,
            themachinescode
        ]
    else:
        all_identities = [
            andrewtatham,
            andrewtathampi,
            andrewtathampi2,
            numberwang_host,
            # julienumberwang,
            # simonnumberwang,
            # eggpunbot,
            # whenmensday,
            # botgleartist,
            # themachinescode
        ]
    import twitterpibot.bootstrap

    twitterpibot.bootstrap.run(all_identities)
