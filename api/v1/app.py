#!/usr/bin/python3

from flask import Flask, make_response, render_template, session, request, redirect, url_for, jsonify
from views.app_views import app_views
from models import storage
from flask_cors import CORS
import uuid

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = "feeya"



@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route("/", strict_slashes=False, methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user = request.form["user_name"]
        status = storage.check_user_name("User", user)
        if status != "Nil":
            pas = status.password
            if pas != request.form["password"]:
                c_id = uuid.uuid4()
                return render_template("home.html", c_id=c_id, status="Invalid password")
            session["role"] = status.role
            session["user_name"] = user
            if status.role == "staff":
                return redirect(url_for("dashbord"))
            elif status.role == "admin":
                return redirect(url_for("admin"))

        else:
            c_id = uuid.uuid4()
            res = "Invalid User"
            return render_template("home.html", c_id=c_id, status=res)
    else:
        c_id = uuid.uuid4()
        return render_template("home.html", c_id=c_id, status="")


@app.route("/user/<id>", strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def user(id):

    if "user_name" in session:
        if session["role"] == "admin" or (session["role"] == "staff" and request.json.get("password") != None ):
            if request.method == "PUT":
                user = storage.check_id("User", id)
                if user != "Nil":
                    res = storage.update("User", id, **request.json)
                    return res
    


    
            if "id" in request.json:
                id = request.json.get("id")
            else:
                return "No id found"
            usr = storage.check_id("User", id)
            if usr == "Nil":
                abort(400, "Id Not Found")
            if request.method == "GET":
                return jsonify([usr.to_dict()])

            if request.method == "DELETE":
                storage.delete("User", id)
                return "deleted Successfully"

    return render_template("home.html", c_id=c_id, status="")

@app.route("/dashbord/", strict_slashes=False)
def dashbord():
    if "user_name" in session:
        user = storage.check_user_name("User", session["user_name"])
        if user.role == "staff":
            return render_template("dashbord.html", user=user, storage=storage)
    return redirect(url_for("home"))

@app.route("/register", strict_slashes=False)
def register():
    if "user_name" in session:
        if session["role"] == "admin":
            return render_template("register.html")
    return redirect(url_for("home"))


@app.route("/admin/", strict_slashes=False)
def admin():
    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        if user.role == "admin":
            return render_template("admin.html", storage=storage, user=user)
    return redirect(url_for("home"))


@app.route("/transections/", strict_slashes=False)
def transections():
    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        return render_template("transection.html", id=user.id, user=user, storage=storage)
    return redirect(url_for("home"))

@app.route("/add_record/", strict_slashes=False)
def add():
    if "user_name" in session:
        user = session["user_name"]
        user = storage.check_user_name("User", user)
        if user.role == "staff":
            return render_template("add_record.html", user=user)
    return redirect(url_for("home"))

@app.route("/user_home/", strict_slashes=False)
def user_home():
    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        if user.role == "staff":
            return render_template("user_home.html", user=user, storage=storage)
    return redirect(url_for("home"))

@app.route("/admin_transactions", strict_slashes=False)
def admin_t():
    if "user_name" in session:
        user_name = session["user_name"]
        if session["role"] == "admin":
            return render_template("admin_transaction.html", storage=storage)
    return redirect(url_for("home"))

@app.route("/admin_users", strict_slashes=False)
def admin_u():
    if "user_name" in session:
        user_name = session["user_name"]
        if session["role"] == "admin":
            return render_template("admin_users.html", storage=storage)
    return redirect(url_for("home"))

@app.route("/admin_home/", strict_slashes=False)
def ad_home():
    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        if user.role == "admin":
            return render_template("admin_home.html", storage=storage, user=user)
    return redirect(url_for("home"))

@app.route("/logout", strict_slashes=False)
def logout():
    session.pop("user_name", None)
    return redirect(url_for("home"))


@app.teardown_appcontext
def treardown(exc):
    storage.close()

@app.errorhandler(404)
def errorhandler(error):
    err = {"error": "Not Found!!"}
    return make_response(err)


if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)
