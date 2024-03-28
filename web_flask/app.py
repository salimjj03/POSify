#!/usr/bin/python3


from flask import Flask, render_template
from models import storage
from models import *


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    dic = []
    users = storage.all("User")
    for k, v in users.items():
        dic.append(v)
    return render_template("home.html", dic=dic)

@app.route("/users", strict_slashes=False)
def users():
    dic = {}
    users = storage.all("User")
    for k, v in users.items():
        dic[k] = v.to_dict()
    return dic

@app.route("/transactions")
@app.route("/transactions/<type>")
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

@app.route("/user/<id>", strict_slashes=False)
def user(id):
    key = "User.{}".format(id)
    users = storage.all("User")
    for k, v in users.items():
        if k == key:
            return v.to_dict()
    return "User Not Found"


@app.route("/all/<user_id>/", strict_slashes=False)
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


@app.route("/withdraw/<user_id>/", strict_slashes=False)
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



if __name__ == "__main__":
    app.run(port=5000, debug=True)
