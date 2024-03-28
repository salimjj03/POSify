#!/usr/bin/python3


from flask import Flask, render_template
from models import storage
from api.v1.views.app_views import app_views


@app_views.route("/transactions", strict_slashes=False)
@app_views.route("/transactions/<type>", strict_slashes=False)
def transactions(type=None):
    dic = {}
    if type:
        result = storage.all(type)
        for k, v in result.items():
            dic[k] = v.to_dict()
        return dic

    result = storage.all()
    for k, v in result.items():
        dic[k] = v.to_dict()
    return dic

