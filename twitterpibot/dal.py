import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twitterpibot.logic import fsh

from twitterpibot.model import Base, Token

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

folder = fsh.root + "temp" + os.sep + "db" + os.sep
fsh.ensure_directory_exists(folder)
_engine = create_engine("sqlite:///" + folder + "twitterpibot.db")
Base.metadata.bind = _engine
Base.metadata.create_all(_engine)


def _create_session():
    DBSession = sessionmaker(bind=_engine)
    session = DBSession()
    return session


def get_token(key, ask=True):
    session = _create_session()
    token = session.query(Token).filter(Token.key == key).first()

    if token:
        return token.value
    elif ask:
        value = None
        while not value:
            value = input("Enter your " + key + ": ")
        set_token(key, value)
        return value
    else:
        return None


def set_token(key, value):
    session = _create_session()
    token = session.query(Token).filter(Token.key == key).first()
    if not token:
        token = Token(key, value)
        session.add(token)
    else:
        token.value = value
    session.commit()


def import_tokens():
    set_token("wordnik api", fsh.get_key("wordnik"))
    set_token("wordnik username", fsh.get_username("wordnik"))
    set_token("wordnik password", fsh.get_password("wordnik"))

    set_token("google api", fsh.get_key("google"))
    set_token("google cse", fsh.get_key("google custom search id"))
    set_token("google secret", fsh._get("secret", "google"))
    for screen_name in [
        "andrewtatham",
        "andrewtathampi",
        "andrewtathampi2",
        "numberwang_host",
        "JulieNumberwang",
        "SimonNumberwang",
        "eggpunbot",
        "WhenMensDay"
    ]:
        set_token("twitter app key " + screen_name, fsh._get("token", screen_name + "_APP_KEY"))
        set_token("twitter app secret " + screen_name, fsh._get("token", screen_name + "_APP_SECRET"))
        set_token("twitter final key " + screen_name, fsh._get("token", screen_name + "_FINAL_OAUTH_TOKEN"))
        set_token("twitter final secret " + screen_name, fsh._get("token", screen_name + "_FINAL_OAUTH_TOKEN_SECRET"))

    session = _create_session()
    tokens = session.query(Token).all()
    for token in tokens:
        print("{key}: {value}".format(**token.__dict__))


if __name__ == "__main__":
    pass
