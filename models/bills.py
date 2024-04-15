#!/usr/bin/python3
""" this is the bills module. """


from models.base import Base, base_db
from sqlalchemy import Column, String, Double, ForeignKey


class Bills(Base, base_db):
    """ This is the bills class that will be used to
    create abjects of thr class. """

    __tablename__ = "bills"

    user_id = Column(
            String(60),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
            )
    amount = Column(Double, nullable=False)
    charges = Column(Double, nullable=False)
    profit = Column(Double, nullable=False)

    def __init__(self, *args, **kwargs):
        """ This is the custructor method that will automatically
        assign the attribute when the object of the class is created. """

        super().__init__(*args, **kwargs)

        self.profit = self.charges
