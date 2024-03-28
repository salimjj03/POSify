#!/usr/bin/python3
""" This is the file engine. """

import json


class File_storage():
    """ This the sile storage class. """

    __file_name = "file.json"
    __data = []


    def save(self, obj):
        """ This method create a new engine. """

        obj_key = "{}.{}".format(
                obj.__class__.__name__,
                obj.id
                )
        dic = {obj_key: str(obj)}
        self.__data.append(dic)
        with open(self.__file_name, "w") as file:
            json.dump(self.__data, file)

    def all(self, cls=None):
        """ This method return all the object. """

        return self.__data

    
    def update(self):
        """ This method update the record. """

        pass


    def delete(self, obj=None):
        """ This method delete the object. """

        pass

    def reload(self):
        """ This method reload the record. """

        try:
            with open(self.__file_name, "r") as file:
                self.__data = json.load(file)
        except Exception:
            pass
