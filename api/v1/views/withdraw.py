#!/usr/bin/python3


from flask import Flask, render_template, request, jsonify
from models import storage
from api.v1.views.app_views import app_views


@app_views.route("/withdraw/<user_id>/", strict_slashes=False)
def withdraw(user_id):
    result = storage.check_id("User", user_id)
    if result == "Nil":
        return "invalid User id"

    ls = []
    wthdrws = storage.all("Withdraw")
    for k, v in wthdrws.items():
        if v.user_id == user_id:
            ls.append(v.to_dict())
    return ls

@app_views.route("/transaction/<user_id>/", strict_slashes=False, methods=["POST"])
def add(user_id):  
    result = storage.check_id("User", user_id)
    if result == "Nil":
        return "invalid User id"
   
    data = request.json
    dic = data
    storage.save(dic)
    return "ok"
