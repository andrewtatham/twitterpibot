import logging
import pprint

import flask
import colorama

from twitterpibot import hardware, controller, tasks, schedule

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

# import textblob.download_corpora
#
# textblob.download_corpora.download_lite()


__author__ = 'andrewtatham'
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
    _shutdown_server()
    logger.info('Server shutting down...')


def _shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


logger = logging.getLogger(__name__)
all_identities = []


def run(identities):
    global all_identities
    all_identities = identities
    obviousness = "=" * 5
    logger.info(obviousness + " Starting " + obviousness)

    logger.info("Setting tasks")
    tasks.set_tasks(all_identities)
    logger.info("Setting schedule")
    schedule.set_scheduled_jobs(all_identities)
    logger.info("Starting tasks")
    tasks.start()
    logger.info("Starting schedule")
    schedule.start()

    logger.info(obviousness + " Starting UI " + obviousness)
    app.run(debug=False, host='0.0.0.0')
    logger.info(obviousness + " Stopped UI " + obviousness)

    logger.info("Stopping schedule")
    schedule.stop()
    logger.info("Stopping tasks")
    tasks.stop()
    logger.info("Stopping hardware")
    hardware.stop()

    logger.info(obviousness + " Stopped " + obviousness)
