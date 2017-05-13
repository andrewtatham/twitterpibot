import logging
import pprint
import random

import flask

from twitterpibot import controller
from twitterpibot.hardware import myhardware

logger = logging.getLogger(__name__)
app = flask.Flask("twitterpibot")

ok = flask.Response(status=200)


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
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/identity/<id_str>')
def identity(id_str):
    retval = {"identity": controller.get_identity(id_str)}
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/following')
def following():
    retval = {"following": controller.get_following()}
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/followinggraph')
def following_graph():
    retval = {"followinggraph": controller.get_following_graph()}
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/exceptions')
def exceptions():
    retval = {
        "exceptions": controller.get_exceptions(),
        "exceptions_chart_data": controller.get_exceptions_chart_data()
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/exceptionsummary')
def exceptionsummarys():
    retval = {
        "exceptionsummary": controller.get_exception_summary()
    }
    logger.debug(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/follow', methods=['POST'])
def follow():
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.follow(identity_id, user_id)
    return ok


@app.route('/unfollow', methods=['POST'])
def unfollow():
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.unfollow(identity_id, user_id)
    return ok


@app.route('/block', methods=['POST'])
def block():
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.block(identity_id, user_id)
    return ok


@app.route('/report', methods=['POST'])
def report():
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.report(identity_id, user_id)
    return ok


@app.route('/shutdown')
def shutdown():
    _shutdown_server()
    logger.info('Server shutting down...')
    return flask.render_template('shutdown.html')


def run():
    if myhardware.is_windows:
        host = "localhost"
    else:
        host = "0.0.0.0"
    app.run(debug=False, host=host)


def _shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    import identities_pis

    pi = identities_pis.AndrewTathamPiIdentity()
    pi2 = identities_pis.AndrewTathamPi2Identity()

    pi.users.get_users(random.sample(pi.users.get_followers(), 10))
    pi.users.score_users(5)
    pi.users.score_users(5)

    pi2.users.get_users(random.sample(pi.users.get_followers(), 10))
    pi2.users.score_users(5)
    pi2.users.score_users(5)

    controller.set_identities([pi, pi2])

    run()
