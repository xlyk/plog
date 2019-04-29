import logging
import os
import signal
import sys
from flask import Flask, render_template
from flask_pymongo import PyMongo


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


class Post:
    def get_all(self):
        for p in mongo.db.posts.find().limit(5):
            p["created"] = p["_id"].generation_time.strftime("%c")
            yield p

    def create(self):
        # todo: check for duplicate title
        post = {"title": "", "content": "", "image": "", "slug": "", "tags": []}
        mongo.db.posts.insert_one(post)


@app.route("/")
def index():
    posts = list(Post().get_all())
    return render_template("index.html", posts=posts)


def shutdown(signal_number, stack_frame):
    app.logger.info(f"Shutting down...")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    app.logger.info(f"Starting...")
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
