#!/usr/bin/python3

from flask import Flask, make_response, render_template
from views.app_views import app_views
from models import storage
from flask_cors import CORS
import uuid

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def home():
    c_id = uuid.uuid4()
    return render_template("home.html", c_id=c_id)

@app.route("/dashbord/<user_name>", strict_slashes=False)
def dashbord(user_name):
    user = storage.check_user_name("User", user_name)
    return render_template("dashbord.html", user=user, storage=storage)

@app.route("/register", strict_slashes=False)
def register():
    return render_template("register.html")


@app.route("/admin/<user_name>", strict_slashes=False)
def admin(user_name):
    user = storage.check_user_name("User", user_name)
    if user == "Nil":
        return "Not found"
    return render_template("admin.html", storage=storage, user=user)


@app.teardown_appcontext
def treardown(exc):
    storage.close()

@app.errorhandler(404)
def errorhandler(error):
    err = {"error": "Not Found!!"}
    return make_response(err)


if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)
