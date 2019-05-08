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
    if not check_session():
        return logout_response()

    return render_template("dashboard.html", posts=Post.get_all())


@app.route("/admin/create/", methods=["GET", "POST"])
def create_post():
    """create post"""
    if not check_session():
        return logout_response()

    if request.method == "POST":
        Post.create(
            title=request.form.get("title"), content=request.form.get("content")
        )
        response = make_response("")
        response.headers["location"] = "/admin/dashboard/"
        return response, 302

    return render_template("create.html")


@app.route("/admin/edit/<post_id>/", methods=["GET", "POST"])
def edit_post(post_id):
    """edit post"""
    if not check_session():
        return logout_response()

    if request.method == "POST":
        # update post
        Post.update(
            post_id=post_id,
            title=request.form.get("title"),
            content=request.form.get("content"),
        )

    post = Post.get_by_id(post_id)
    return render_template("edit.html", post=post)


@app.route("/admin/logout/", methods=["GET"])
def logout():
    """logout admin user"""
    return logout_response()


def check_session():
    """returns true if session cookie is valid"""
    session = request.cookies.get("session")
    user_obj = User.get_by_session(session)
    return bool(user_obj)


def logout_response():
    """returns response that unsets cookie"""
    response = make_response("")
    response.set_cookie("session", "", expires=0)
    response.headers["location"] = "/admin/login/"
    return response, 302


def shutdown(signal_number, stack_frame):
    app.logger.info(f"Shutting down...")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    app.logger.info(f"Starting...")
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
