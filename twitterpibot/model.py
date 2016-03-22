from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Token(Base):
    __tablename__ = 'token'
    key = Column(String(250), primary_key=True)
    value = Column(String(250))

    def __init__(self, key, value):
        self.key = key
        self.value = value


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    screen_name = Column(String(250))


class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    text = Column(String(250))

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship(User)
