from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

ModelBase = declarative_base()


class User(ModelBase):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    screen_name = Column(String(250))


class Tweet(ModelBase):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    text = Column(String(250))

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship(User)


class ExceptionRow(ModelBase):
    __tablename__ = 'exception'
    id = Column(Integer, primary_key=True)
    now = Column(DateTime())
    uptime = Column(Float())
    boottime = Column(DateTime())
    log_type = Column(String(50))
    screen_name = Column(String(50))
    message = Column(String(100))
    stack_trace = Column(String(250))
