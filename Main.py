import pprint
import sys
import logging

import flask

import twitterpibot
import twitterpibot.Controller
app = flask.Flask("twitterpibot")

controller = twitterpibot.Controller.Controller()
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/init')
def init():
    retval = {
        "actions": controller.get_actions(),
        "identities": controller.get_identities()
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/identity')
@app.route('/identity/<screen_name>')
def identity(screen_name=None):
    retval = {"identities": controller.get_identities(screen_name)}
    return flask.jsonify(retval)


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

twitterpibot.start()
logger.info("Starting UI")
app.run(debug=True, host='0.0.0.0')
logger.info("Stopped UI")
twitterpibot.stop()

sys.exit(0)
