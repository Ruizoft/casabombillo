from app import Base
from sqlalchemy import Column, Integer, String

class User(Base):

    __tablename__ = 'users'

    # User Name
    id = Column(Integer, primary_key=True)

    name    = Column(String(128),  nullable=False)

    # Identification Data: email & password
    email    = Column(String(128),  nullable=False,
                                            unique=True)
    password = Column(String(192),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)