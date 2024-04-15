#!/usr/bin/python3
""" This is the withdraw model. """

from models.base import Base, base_db
from sqlalchemy import Column, Double, create_engine, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Withdraw(Base, base_db):
    """ This is the withdraw class that will be
    used to create object of the class. """

    __tablename__ = "withdraws"
    user_id = Column(
            String(60),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
            )
    amount = Column(Double, nullable=False)
    charges = Column(Double, nullable=False)
    profit = Column(Double, nullable=False)
    __deductions = 0.0

    def __init__(self, *args, **kwargs):
        """ This is the custructor method that will automatically
        assign the attribute when the object of the class is created. """

        super().__init__(*args, **kwargs)
        if args:
            self.amount = args[0]
            self.charges = args[1]
        self.__deductions = (self.amount * 0.5) / 100
        self.profit = self.charges - self.__deductions
