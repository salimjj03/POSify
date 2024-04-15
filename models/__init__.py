#!/usr/bin/python3
""" this module will automatically run and create the
and create the storage abject, """

from models.engine.db_engine import Db_storage


storage = Db_storage()
storage.reload()
