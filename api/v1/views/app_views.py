#!/usr/bin/python3


from flask import Flask, Blueprint


app_views = Blueprint("app_views", __name__)


from api.v1.views.withdraw import *
from api.v1.views.user import *
from api.v1.views.transactions import *

