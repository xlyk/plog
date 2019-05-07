import logging
import os
import signal
import sys

from flask import Flask, request, render_template, make_response, redirect
from flask_pymongo import PyMongo

from . import data
from .data import User, Post

# environment variables
LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
DEBUG_MODE = bool(os.getenv("DEBUG_MODE"))
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# initialize logging
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s")
log_level = getattr(logging, LOG_LEVEL.upper())

# initialize flask app
app = Flask("plog", template_folder="/app/src/templates")
app.config.update(DEBUG=DEBUG_MODE)
app.logger.setLevel(log_level)
logging.getLogger("werkzeug").setLevel(log_level)

# initialize database
app.config["MONGO_URI"] = DB_CONNECTION_STRING

# setup db
data.mongo = PyMongo(app)


@app.route("/")
def index():
    """main page"""

    posts = Post.get_recent(limit=5)
    return render_template("index.html", posts=posts)


@app.route("/admin/login/", methods=["GET", "POST"])
def login():
    """admin login"""

    # redirect existing sessions to dashboard
    if User.get_by_session(session=request.cookies.get("session")):
        return redirect("/admin/dashboard/", code=302)

    # handle GET request
    if request.method == "GET":
        return render_template("login.html")

    # attempt to login user
    try:
        user = User(**request.form).login()
    except KeyError:
        return "invalid post data", 400
    except ValueError:
        return "login failed", 401

    # return response with session cookie
    response = make_response("", 200)
    response.set_cookie("session", user["session"])
    response.headers["location"] = "/admin/dashboard/"
    return response, 302


@app.route("/admin/dashboard/", methods=["GET"])
def dashboard():
    """admin dashboard"""

    # check for session cookie
    session = request.cookies.get("session")
    user_obj = User.get_by_session(session)
    if not user_obj:
        # delete session cookie
        response = make_response("")
        response.set_cookie("session", "", expires=0)
        response.headers["location"] = "/admin/login/"
        return response, 302

    return render_template("dashboard.html", posts=Post.get_all())


def new_post():
    """create post"""


def edit_post():
    """edit post"""


def shutdown(signal_number, stack_frame):
    app.logger.info(f"Shutting down...")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    app.logger.info(f"Starting...")
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
