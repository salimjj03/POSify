#!/usr/bin/python3
""" This is the flask app module. """

from flask import Flask, make_response, render_template
from flask import session, request, redirect, url_for, jsonify
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
    """  this method ensures that for every HTTP response
    generated by the Flask application, the Cache-Control
    header is set to 'no-store', instructing clients not
    to cache the response. """

    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route("/", strict_slashes=False, methods=["GET", "POST"])
def home():
    """ This method return the home route which contain
    the login form if the request method is GET else if
    the return method if POST it will return the user dashbord. """

    if request.method == "POST":
        user = request.form["user_name"]
        status = storage.check_user_name("User", user)
        if status != "Nil":
            pas = status.password
            if pas != request.form["password"]:
                c_id = uuid.uuid4()
                return render_template(
                        "home.html",
                        c_id=c_id,
                        status="Invalid password")
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


@app.route(
        "/user/<id>",
        strict_slashes=False,
        methods=["GET", "DELETE", "PUT"]
        )
def user(id):
    """ this endpoint is used to update user if method is PUT,
    else if method is DELELE it will delete the user. """

    if "user_name" in session:
        if session["role"] == "admin" or (session["role"] == "staff" and request.json.get("password") is not None):
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
    """ this endpoint return the user dashbord base
    on the role of the user. """

    if "user_name" in session:
        user = storage.check_user_name("User", session["user_name"])
        if user.role == "staff":
            return render_template("dashbord.html", user=user, storage=storage)
    return redirect(url_for("home"))


@app.route("/register", strict_slashes=False)
def register():
    """ this endpoit contain the form to register new
    user. """

    if "user_name" in session:
        if session["role"] == "admin":
            return render_template("register.html")
    return redirect(url_for("home"))


@app.route("/admin/", strict_slashes=False)
def admin():
    """ this endpoit is the admin dashord. """

    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        if user.role == "admin":
            return render_template("admin.html", storage=storage, user=user)
    return redirect(url_for("home"))


@app.route("/transections/", strict_slashes=False)
def transections():
    """ the transaction endpoint. """

    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        return render_template(
                "transection.html",
                id=user.id,
                user=user,
                storage=storage
                )
    return redirect(url_for("home"))


@app.route("/add_record/", strict_slashes=False)
def add():
    """ the endpoint that is used to add record. """

    if "user_name" in session:
        user = session["user_name"]
        user = storage.check_user_name("User", user)
        if user.role == "staff":
            return render_template("add_record.html", user=user)
    return redirect(url_for("home"))


@app.route("/user_home/", strict_slashes=False)
def user_home():
    """ the endpoint that contain the user welcom page. """

    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        if user.role == "staff":
            return render_template(
                    "user_home.html",
                    user=user,
                    storage=storage
                    )
    return redirect(url_for("home"))


@app.route("/admin_transactions", strict_slashes=False)
def admin_t():
    """ the endpoint that contain admin transaction page. """

    if "user_name" in session:
        user_name = session["user_name"]
        if session["role"] == "admin":
            return render_template(
                    "admin_transaction.html",
                    storage=storage
                    )
    return redirect(url_for("home"))


@app.route("/admin_users", strict_slashes=False)
def admin_u():
    """ the endpoint that contain the admin users page. """

    if "user_name" in session:
        user_name = session["user_name"]
        if session["role"] == "admin":
            return render_template("admin_users.html", storage=storage)
    return redirect(url_for("home"))


@app.route("/admin_home/", strict_slashes=False)
def ad_home():
    """ this endpoint contain admin home page. """

    if "user_name" in session:
        user_name = session["user_name"]
        user = storage.check_user_name("User", user_name)
        if user.role == "admin":
            return render_template(
                    "admin_home.html",
                    storage=storage,
                    user=user
                    )
    return redirect(url_for("home"))


@app.route("/logout", strict_slashes=False)
def logout():
    """ this endpoint is used to logout from user. """

    session.pop("user_name", None)
    return redirect(url_for("home"))


@app.teardown_appcontext
def treardown(exc):
    """ The application context in Flask is typically
    created at the beginning of a request and torn
    down after the request has been handled."""

    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """ this method is used to handle 404 error. """

    err = {"error": "Not Found!!"}
    return make_response(err)


if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)
