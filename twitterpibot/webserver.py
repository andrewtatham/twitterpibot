import logging
import random

import flask

from twitterpibot import controller

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
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/actions')
def actions():
    retval = {
        "actions": controller.get_actions(),
    }
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/identities')
def identities():
    retval = {"identities": controller.get_identities()}
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/identity/<id_str>')
def identity(id_str):
    retval = {"identity": controller.get_identity(id_str)}
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/following')
def following():
    retval = {"following": controller.get_following()}
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/followinggraph')
def following_graph():
    retval = {"followinggraph": controller.get_following_graph()}
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/exceptions')
def exceptions():
    retval = {
        "exceptions": controller.get_exceptions(),
        "exceptions_chart_data": controller.get_exceptions_chart_data()
    }
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/exceptionsummary')
def exceptionsummarys():
    retval = {
        "exceptionsummary": controller.get_exception_summary()
    }
    logger.debug(retval)
    return flask.jsonify(retval)


@app.route('/follow', methods=['POST'])
def follow():
    logger.info(flask.request.json)
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.follow(identity_id, user_id)
    return ok


@app.route('/unfollow', methods=['POST'])
def unfollow():
    logger.info(flask.request.json)
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.unfollow(identity_id, user_id)
    return ok


@app.route('/block', methods=['POST'])
def block():
    logger.info(flask.request.json)
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.block(identity_id, user_id)
    return ok


@app.route('/report', methods=['POST'])
def report():
    logger.info(flask.request.json)
    identity_id = flask.request.json["identity_id"]
    user_id = flask.request.json["user_id"]
    controller.report(identity_id, user_id)
    return ok


@app.route('/shutdown')
def shutdown():
    _shutdown_server()
    logger.info('Server shutting down...')


def _shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import identities

    pi = identities.AndrewTathamPiIdentity()
    pi2 = identities.AndrewTathamPi2Identity()

    pi.users.get_users(random.sample(pi.users.get_followers(), 10))
    pi.users.score_users(5)

    pi2.users.get_users(random.sample(pi.users.get_followers(), 10))
    pi2.users.score_users(5)

    controller.set_identities([pi, pi2])

    app.run(debug=False, host='0.0.0.0')
