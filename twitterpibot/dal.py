from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twitterpibot.model import Base, Token

_engine = create_engine('sqlite:///twitterpibot.db')
Base.metadata.bind = _engine
Base.metadata.create_all(_engine)
DBSession = sessionmaker(bind=_engine)


def create_session():
    session = DBSession()
    return session


def get_token(key):
    session = create_session()
    token = session.query(Token).filter(Token.key == key).first()
    if token:
        return token.value
    else:
        return None


def set_token(key, value):
    session = create_session()
    token = session.query(Token).filter(Token.key == key).first()
    if not token:
        token = Token(key, value)
        session.add(token)
    else:
        token.value = value
    session.commit()


if __name__ == "__main__":
    key = "twitter"
    print(get_token(key))
    set_token(key,"blah")
    print(get_token(key))
    

