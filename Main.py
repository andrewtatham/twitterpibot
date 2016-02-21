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


@app.route('/demo')
def demo():
    return flask.render_template('demo.html')


@app.route('/init')
def init():
    retval = {
        "actions": controller.get_actions(),
        "identities": controller.get_identities()
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/actions')
def actions():
    retval = {
        "actions": controller.get_actions(),
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/identities')
def identities():
    retval = {"identities": controller.get_identities()}
    return flask.jsonify(retval)


@app.route('/identity/<screen_name>')
def identity(screen_name):
    retval = {"identity": controller.get_identity(screen_name)}
    return flask.jsonify(retval)


@app.route('/following')
def following():
    retval = {"following": controller.get_following()}
    return flask.jsonify(retval)

@app.route('/followinggraph')
def following_graph():
    retval = {"followinggraph": controller.get_following_graph()}
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
