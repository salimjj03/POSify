#!/usr/bin/python3

from models.base import Base, base_db
from sqlalchemy import String, Column, Integer, Numeric

class User(Base, base_db):

    __tablename__ = "users"
    full_name = Column(String(20), nullable=False)
    user_name = Column(String(20), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    gender = Column(String(20), nullable=False)
    role = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            self.full_name = args[0]
            self.user_name = args[1]
            self.password = args[2]
