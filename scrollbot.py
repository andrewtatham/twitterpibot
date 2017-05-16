from twitterpibot import loggingconfig

loggingconfig.init()

if __name__ == '__main__':
    from twitterpibot.logic import fsh
    from twitterpibot.data_access import dal

    # dal.import_tokens(fsh.root + "tokens.csv")
    dal.export_tokens(fsh.root + "tokens.csv")

if __name__ == "__main__":
    from identities import AndrewTathamIdentity
    from identities_scrollbot import ScrollBotIdentity

    andrewtatham = AndrewTathamIdentity(stream=False)
    scrollbot = ScrollBotIdentity(andrewtatham)

    andrewtatham.buddies = [
        scrollbot
    ]

    all_identities = [
        andrewtatham,
        scrollbot
    ]

    import twitterpibot.bootstrap

    twitterpibot.bootstrap.run(all_identities)
