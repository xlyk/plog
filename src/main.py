import logging
import os
import signal
import sys

from flask import Flask, request, render_template, make_response
from flask_pymongo import PyMongo

from . import data

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
    posts = data.Post.get_recent(limit=5)
    return render_template("index.html", posts=posts)


@app.route("/admin/login/", methods=["GET", "POST"])
def login():
    # check for session cookie
    session = request.cookies.get("session")
    existing = data.User.get_by_session(session)
    if existing:
        return "u already logged in"

    # handle GET request
    if request.method == "GET":
        return render_template("login.html")

    # attempt to login user
    try:
        user = data.User(**request.form)
        user.login()
    except KeyError:
        return "invalid post data", 400
    except ValueError:
        return "login failed", 401

    # return response with session cookie
    ret = f"wow nice job, {user['username']}"
    response = make_response(ret, 200)
    response.set_cookie("session", user["session"])
    return response


def shutdown(signal_number, stack_frame):
    app.logger.info(f"Shutting down...")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    app.logger.info(f"Starting...")
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
