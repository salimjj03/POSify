#!/usr/bin/python3


from flask import Flask, render_template, abort, jsonify, request
from models import storage
from api.v1.views.app_views import app_views
from models.withdraw import Withdraw
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def users():

    if request.method == "GET":

        dic = []
        users = storage.all("User")
        for k, v in users.items():
            dic.append(v.to_dict())
        return jsonify(dic)

    if request.method == "POST":

        data = request.get_json()
        if data is None:
            return "Not a Json"
        if data.get("full_name") == "":
            return "full name missing"
        if data.get("user_name") == "":
            return "user name missing"
        if data.get("password") == "":
            return"password missing"
        obj = User(**data)
        if storage.save(obj) == "exist":
            return"User name exist"
        return "{} created Successfully".format(data.get("full_name"))

"""
@app_views.route("/user/<id>", strict_slashes=False, methods=["GET", "DELETE", "POST"])
def user(id):


    if request.method == "POST":
        status = storage.check_user_name(User, id)
        if status != "Nil":
            pas = request.json.get('password')
            if status.password == pas:
                if status.role == None:
                    return "no role"
                else:
                    return status.role
            else:
                return "invalid password"
        else:
                return "invalid user"

    usr = storage.check_id("User", id)
    if usr == "Nil":
        abort(400, "Id Not Found")
    if request.method == "GET":
        return jsonify([usr.to_dict()])

    if request.method == "DELETE":
        storage.delete("User", id)
        return jsonify({"delete: Successfully"})
"""

@app_views.route("/all/<user_id>/", strict_slashes=False, methods=["GET"])
def all(user_id):
    result = storage.check_id("User", user_id)
    if result == "Nil":
        return "invalid User id"

    ls = []
    wthdrws = storage.all()
    for k, v in wthdrws.items():
        if k.split(".")[0] != "User":
            if v.user_id == user_id:
                ls.append(v.to_dict())
    return ls

