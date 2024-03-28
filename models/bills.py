#!/usr/bin/python3


from models.base import Base, base_db
from sqlalchemy import Column, String, Double, ForeignKey

class Bills(Base, base_db):

    __tablename__ = "bills"

    user_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Double, nullable=False)
    charges = Column(Double, nullable=False)
    profit = Column(Double, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.profit = self.charges

