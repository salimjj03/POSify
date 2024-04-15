#!/usr/bin/python3
""" This is the storage module. """


from models.base import base_db
from models.user import User
from models.deposit import Deposit
from models.withdraw import Withdraw
from models.bills import Bills
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Db_storage():
    """ this is storage class that will be used to
    create a storage object that will handle storing,
    updating, delete etc. """

    __engine = None
    __session = None

    def __init__(self):
        """ This is the custructor method that will automatically
        assign the attribute when the object of the class is created. """

        self.__engine = create_engine(
                "mysql+mysqldb://salem:root@localhost/pos"
                )
        base_db.metadata.create_all(bind=self.__engine)

    def all(self, clas=None):
        """ this method return a dictionary of all object of the classes
        if class is None, else it return a dictionary of all object of
        the giving class. """

        dic = {}
        classes = ["Withdraw", "User", "Deposit", "Bills"]

        if clas:
            if type(clas) == str:
                if clas not in classes:
                    return "Invalid Transaction Type"
                clas = globals()[clas]
            result = self.__session.query(clas).all()
            for obj in result:
                key = "{}.{}".format(
                        obj.__class__.__name__,
                        obj.id
                        )
                dic[key] = obj
            return dic

        classes = [User, Withdraw, Deposit, Bills]
        for cls in classes:
            result = self.__session.query(cls).all()
            for obj in result:
                key = "{}.{}".format(
                        obj.__class__.__name__,
                        obj.id
                        )
                dic[key] = obj
        return dic

    def save(self, obj):
        """ This method is used to add obj to the database. """

        if type(obj) is dict:
            cls = obj.get("class")
            cls = globals()[cls]
            del obj["class"]
            new_obj = cls(**obj)
            self.__session.add(new_obj)
            self.__session.commit()
            return

        if obj.__class__.__name__ == "User":
            result = self.all(User)
            for k, v in result.items():
                if v.user_name == obj.user_name:
                    print("User name Exist")
                    return "exist"
        self.__session.add(obj)
        self.__session.commit()

    def update(self, cls, id, **kwargs):
        """ This method used dictionary to update an object using the id
        of the object base on the class of the object. """

        if type(cls) == str:
            cls = globals()[cls]
        result = self.__session.query(cls).filter_by(id=id).first()
        if result:
            for k, v in kwargs.items():
                if k in result.to_dict():
                    if k == "full_name":
                        result.full_name = v
                    elif k == "phone_number":
                        if len(v) != 11:
                            return "invalid phone number"
                        for ky, vl in self.all("User").items():
                            if vl.phone_number == v:
                                return "phone number exits"
                        result.phone_number = v
                    elif k == "password":
                        result.password = v
                    elif k == "amount":
                        result.amount = v
                    elif k == "charges":
                        result.charges = v
                    elif k == "gender":
                        result.gender = v
                    elif k == "role":
                        result.role = v
                    else:
                        return "invalid key"
            self.__session.commit()
            return "{} updated successfully to {}".format(k, v)
        return "in valid id"

    def delete(self, cls, id):
        """ This mothod is used to delete object from the
        database using the object ib based on the class. """

        if type(cls) == str:
            cls = globals()[cls]
        result = self.__session.query(cls).filter_by(id=id).first()
        if result:
            self.__session.delete(result)
            self.__session.commit()
            return "deleted successfully"
        return "invalid id"

    def reload(self):
        """ This method is used to create database session. """

        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def check_id(self, cls, id):
        """ This method is used to check if object exist based on
        the id and return the object,. else return Nil. """

        result = self.all(cls)
        for k, v in result.items():
            if k.split(".")[1] == id:
                return (v)
        return "Nil"

    def check_user_name(self, cls, user_name):
        """ This method is used to check if object exist based on
        the user_name and return the object. else return Nil. """

        result = self.all(cls)
        for k, v in result.items():
            if v.user_name == user_name:
                return v
        return "Nil"

    def profit(self, **kwargs):
        """ This method is used to calculate profit and
        number of transactins. it return dictionary with
        profit and count. """

        dic = {"profit": 0, "count": 0}
        cls = kwargs.get("cls")
        user_id = kwargs.get("user_id")

        if cls is None:
            result = self.all()
        elif cls is not None:
            result = self.all(cls)
        for k, v in result.items():
            if k.split(".")[0] != "User":
                if user_id is not None:
                    if v.user_id == user_id:
                        dic["profit"] = dic["profit"] + v.profit
                        dic["count"] = dic["count"] + 1
                elif user_id is None:
                    dic["profit"] = dic["profit"] + v.profit
                    dic["count"] = dic["count"] + 1

        return (dic)

    def transactions(self, **kwargs):
        """ This method is used to return a dictionary
        with all the transaction. """

        dic = {}
        cls = kwargs.get("cls")
        user_id = kwargs.get("user_id")

        if cls is None:
            result = self.all()
        elif cls is not None:
            result = self.all(cls)

        for k, v in result.items():
            if k.split(".")[0] != "User":
                if user_id is not None:
                    if v.user_id == user_id:
                        key = "{}.{}".format(v.__class__.__name__, v.id)
                        dic[key] = v
                elif user_id is None:
                    key = "{}.{}".format(v.__class__.__name__, v.id)
                    dic[key] = v
        return dic

    def close(self):
        """ This method is used to close the datav=base session. """

        self.__session.remove()
