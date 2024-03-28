#!/usr/bin/python3
""" This is the basemode that will be inheritade
by the classes. """


#import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker

base_db = declarative_base()


class Base():
    """ This is the base model class. """

    id = Column(String(60), primary_key=True)
    create_at = Column(DateTime, default=datetime.utcnow())
    update_at = Column(DateTime, default=datetime.utcnow())


    def __init__(self, *args, **kwargs):
        """ This is the custructor method. """

        if kwargs:
            if id not in kwargs:
                self.id = str(uuid4())
            for k, v in kwargs.items():
                setattr(self,k,v)
        else:
            self.id = str(uuid4())
            self.create_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            self.update_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")



    def to_dict(self):
        """ This method return the dictionary represantation
        of the ofject. """

        dic = self.__dict__.copy()
        dic["class_name"] = self.__class__.__name__
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        return dic

    def save(self):
  #      models.storage.save(self)
        pass

    def update(self):
        """ This method update the object. """
        self.update_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")



    def __str__(self):
       """ this is the method that return the str
       representation of the object. """

       return str(self.to_dict())
