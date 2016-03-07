import pprint
import sys
import logging

import flask

import colorama

import twitterpibot

if not twitterpibot.hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

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

logger.info("Setting tasks")
t = twitterpibot.identities.get_all_tasks()
twitterpibot.tasks.set_tasks(t)
logger.info("Setting schedule")
j = twitterpibot.identities.get_all_scheduled_jobs()
twitterpibot.schedule.set_scheduled_jobs(j)
logger.info("Starting tasks")
twitterpibot.tasks.start()
logger.info("Starting schedule")
twitterpibot.schedule.start()

logger.info("Starting UI")
app.run(debug=False, host='0.0.0.0')
logger.info("Stopped UI")

logger.info("Stopping schedule")
twitterpibot.schedule.stop()
logger.info("Stopping tasks")
twitterpibot.tasks.stop()
logger.info("Stopping hardware")
twitterpibot.hardware.stop()
logger.info("Stopped")

sys.exit(0)
