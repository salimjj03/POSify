#!/usr/bin/python3

from models.base import base_db, Base
from sqlalchemy import Column, String, ForeignKey, Double

class Deposit(Base, base_db):

    __tablename__ = "deposit"
    user_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Double, nullable=False)
    charges = Column(Double, nullable=False)
    profit = Column(Double, nullable=False)
    deduction = 20.0


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profit = self.charges - self.deduction

