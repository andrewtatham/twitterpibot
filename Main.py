import pprint
import sys
import logging

import flask

import twitterpibot


app = flask.Flask("twitterpibot")


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/demo')
def demo():
    return flask.render_template('demo.html')


@app.route('/init')
def init():
    retval = {
        "actions": twitterpibot.controller.get_actions(),
        "identities": twitterpibot.controller.get_identities()
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/actions')
def actions():
    retval = {
        "actions": twitterpibot.controller.get_actions(),
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/identities')
def identities():
    retval = {"identities": twitterpibot.controller.get_identities()}
    return flask.jsonify(retval)


@app.route('/identity/<screen_name>')
def identity(screen_name):
    retval = {"identity": twitterpibot.controller.get_identity(screen_name)}
    return flask.jsonify(retval)


@app.route('/following')
def following():
    retval = {"following": twitterpibot.controller.get_following()}
    return flask.jsonify(retval)


@app.route('/followinggraph')
def following_graph():
    retval = {"followinggraph": twitterpibot.controller.get_following_graph()}
    return flask.jsonify(retval)


@app.route('/shutdown')
def shutdown():
    _shutdown_server()
    logger.info('Server shutting down...')


def _shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


logger = logging.getLogger(__name__)

twitterpibot.start()
logger.info("Starting UI")

app.run(debug=twitterpibot.hardware.is_andrew_macbook, host='0.0.0.0')
logger.info("Stopped UI")
twitterpibot.stop()

sys.exit(0)
