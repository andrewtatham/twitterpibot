import logging

import flask

from twitterpibot import controller

logger = logging.getLogger(__name__)
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


@app.route('/identity/<screen_name>')
def identity(screen_name):
    retval = {"identity": controller.get_identity(screen_name)}
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
    logging.basicConfig(level=logging.DEBUG)
    app.config['SERVER_NAME'] = "localhost:5000"
    app.run(debug=True, host='0.0.0.0')
