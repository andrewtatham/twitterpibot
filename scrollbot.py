from twitterpibot import loggingconfig

loggingconfig.init()

if __name__ == '__main__':
    from twitterpibot.logic import fsh
    from twitterpibot.data_access import dal

    # dal.import_tokens(fsh.root + "tokens.csv")
    dal.export_tokens(fsh.root + "tokens.csv")

if __name__ == "__main__":

    from identities import ScrollBotIdentity


    scrollbot = ScrollBotIdentity()

    import twitterpibot.hardware.myhardware

    if twitterpibot.hardware.myhardware.is_scroll_bot:
        all_identities = [
            scrollbot
        ]
    else:
        all_identities = [
            scrollbot
        ]
    import twitterpibot.bootstrap

    twitterpibot.bootstrap.run(all_identities)
