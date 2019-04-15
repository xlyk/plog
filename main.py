import logging
import os
import signal
import sys
from flask import Flask, render_template

LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
DEBUG_MODE = bool(os.getenv("DEBUG_MODE"))

# initialize logging
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s")
log_level = getattr(logging, LOG_LEVEL.upper())

# initialize flask app
app = Flask("plog")
app.config.update(DEBUG=DEBUG_MODE)
app.logger.setLevel(log_level)
logging.getLogger("werkzeug").setLevel(log_level)


@app.route("/")
def index():
    # TODO: lookup page
    return render_template("index.html")


def shutdown(signal_number, stack_frame):
    app.logger.info(f"Shutting down...")
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    app.logger.info(f"Starting...")
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
