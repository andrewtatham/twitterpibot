import datetime
import os
import random
import traceback

# import uptime
from twitterpibot.data_access import model, tokens

from sqlalchemy.orm import sessionmaker

from twitterpibot.data_access.model import ExceptionRow
from twitterpibot.data_access.tokens import Token
from twitterpibot.logic import fsh

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

folder = fsh.root + "temp" + os.sep + "db" + os.sep
fsh.ensure_directory_exists(folder)

_engine = model.create_engine("sqlite:///" + folder + "twitterpibot.db")
_tokens_engine = tokens.create_engine("sqlite:///" + folder + "tokens.db")

model.ModelBase.metadata.bind = _engine
tokens.TokenBase.metadata.bind = _tokens_engine


model.ModelBase.metadata.create_all(_engine)
tokens.TokenBase.metadata.create_all(_tokens_engine)


def _create_tokens_session():
    dbsession = sessionmaker(bind=_tokens_engine)
    session = dbsession()
    return session


def _create_session():
    dbsession = sessionmaker(bind=_engine)
    session = dbsession()
    return session


def tokens_file_path():
    return None


def get_token(key, ask=True):
    session = _create_tokens_session()
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
    session = _create_tokens_session()
    token = session.query(Token).filter(Token.key == key).first()
    if not token:
        token = Token(key, value)
        session.add(token)
    else:
        token.value = value
    session.commit()


def migrate_tokens():
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


def display_tokens():
    session = _create_tokens_session()
    ts = session.query(Token).all()
    for t in ts:
        print("{key}: {value}".format(**t.__dict__))


def import_tokens(file_name):
    csv = fsh.parse_csv(file_name)
    for row in csv:
        if row:
            print(row)
            set_token(row[0], row[1])


def export_tokens(file_name):
    session = _create_tokens_session()
    ts = session.query(Token).all()
    csv = [(t.key, t.value) for t in ts]
    fsh.write_csv(file_name, csv)


def warning(identity, ex, label):
    _exception(identity, ex, "Warning", label)


def exception(identity, ex, label):
    _exception(identity, ex, "Exception", label)


def _exception(identity, ex, log_type, label):
    session = _create_session()

    row = ExceptionRow()
    row.now = datetime.datetime.now()
    row.uptime = None  # uptime.uptime()
    row.boottime = None  # uptime.boottime()
    row.log_type = log_type
    row.label = label
    if identity:
        row.screen_name = identity.screen_name

    row.message = str(ex)
    row.stack_trace = traceback.format_exc()

    session.add(row)
    session.commit()


def get_exceptions():
    session = _create_session()
    exs = session.query(ExceptionRow).all()
    return exs


if __name__ == "__main__":
    from twitterpibot import exceptionmanager

    try:
        exceptionmanager.raise_test_exception()
    except Exception as ex:
        if random.randint(0, 1) == 0:
            warning(None, ex, str(exceptionmanager.raise_test_exception))
        else:
            exception(None, ex, str(exceptionmanager.raise_test_exception))
