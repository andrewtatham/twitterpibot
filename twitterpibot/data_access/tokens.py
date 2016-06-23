import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

TokenBase = declarative_base()


class Token(TokenBase):
    __tablename__ = 'token'
    key = sqlalchemy.Column(sqlalchemy.String(250), primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.String(250))

    def __init__(self, key, value):
        self.key = key
        self.value = value
