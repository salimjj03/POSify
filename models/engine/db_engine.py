#!/usr/bin/python3


from models.base import base_db
from models.user import User
from models.deposit import Deposit
from models.withdraw import Withdraw
from models.bills import Bills
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Db_storage():
    
    __engine = None
    __session = None


    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://salem:root@localhost/pos")
        base_db.metadata.create_all(bind=self.__engine)

    def all(self, clas=None):

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
            return  result
        return "in valid id"

    def delete(self, cls, id):
        if type(cls) == str:
            cls = globals()[cls]
        result = self.__session.query(cls).filter_by(id=id).first()
        if result:
            self.__session.delete(result)
            self.__session.commit()
            return "deleted successfully"
        return "invalid id"
            

    def reload(self):
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def check_id(self, cls, id):
        result = self.all(cls)
        for k, v in result.items():
            if k.split(".")[1] == id:
                return (v)
        return "Nil"

    def check_user_name(self, cls, user_name):
        result = self.all(cls)
        for k, v in result.items():
            if v.user_name == user_name:
                return v
        return "Nil"


    def profit(self, **kwargs):
        dic = {"profit": 0, "count": 0}
        cls = kwargs.get("cls")
        user_id = kwargs.get("user_id")

        if cls == None:
            result = self.all()
        elif cls != None:
            result = self.all(cls) 

        for k, v in result.items():
            if k.split(".")[0] != "User":
                if user_id != None:
                    if v.user_id == user_id:
                        dic["profit"] = dic["profit"] + v.profit
                        dic["count"] = dic["count"]  + 1
                elif user_id == None:
                    dic["profit"] = dic["profit"] + v.profit
                    dic["count"] = dic["count"]  + 1

        return (dic)

    def transactions(self, **kwargs):
        dic = {}
        cls = kwargs.get("cls")
        user_id = kwargs.get("user_id")

        if cls == None:
            result = self.all()
        elif cls != None:
            result = self.all(cls)

        for k, v in result.items():
            if k.split(".")[0] != "User":
                if user_id != None:
                    if v.user_id == user_id:
                        key = "{}.{}".format(v.__class__.__name__, v.id)
                        dic[key] = v
                elif user_id == None:
                    key = "{}.{}".format(v.__class__.__name__, v.id)
                    dic[key] = v

        return dic        


    def close(self):
        self.__session.remove()
