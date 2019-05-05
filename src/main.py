import datetime
import logging
import os
import signal
import sys
from flask import Flask, request, render_template
from flask_pymongo import PyMongo

import data


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
mongo = PyMongo(app)

# pass mongo instance to data module
data.mongo = mongo


@app.route("/")
def index():
    posts = data.Post.get_recent(limit=5)
    return render_template("index.html", posts=posts)


@app.route("/admin/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = data.User(**request.form)
        except KeyError:
            return "invalid post data", 400

        try:
            user.login()
        except ValueError:
            return "login failed", 401

        return f"wow nice job, {user['username']}"

    return render_template("login.html")


def shutdown(signal_number, stack_frame):
    app.logger.info(f"Shutting down...")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    app.logger.info(f"Starting...")
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
