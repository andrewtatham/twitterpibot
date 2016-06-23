import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

ModelBase = declarative_base()


class User(ModelBase):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    screen_name = sqlalchemy.Column(sqlalchemy.String(250))


class Tweet(ModelBase):
    __tablename__ = 'tweet'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    text = sqlalchemy.Column(sqlalchemy.String(250))

    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    sender = relationship(User)


class ExceptionRow(ModelBase):
    __tablename__ = 'exception'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    now = sqlalchemy.Column(sqlalchemy.DateTime())
    uptime = sqlalchemy.Column(sqlalchemy.Float())
    boottime = sqlalchemy.Column(sqlalchemy.DateTime())
    log_type = sqlalchemy.Column(sqlalchemy.String(50))
    screen_name = sqlalchemy.Column(sqlalchemy.String(50))
    label = sqlalchemy.Column(sqlalchemy.String(50))
    message = sqlalchemy.Column(sqlalchemy.String(100))
    stack_trace = sqlalchemy.Column(sqlalchemy.String(250))
