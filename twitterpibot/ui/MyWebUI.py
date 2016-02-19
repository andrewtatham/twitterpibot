import logging
import pprint

import flask

from twitterpibot.ui.Controller import Controller

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

controller = Controller()


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/init')
def init():
    retval = {
        "actions": controller.get_actions(),
        "identities": controller.get_identities()
    }
    logger.info(pprint.pformat(retval))
    return flask.jsonify(retval)


@app.route('/identity')
@app.route('/identity/<screen_name>')
def identity(screen_name=None):
    retval = {}
    retval["identities"] = controller.get_identities(screen_name)
    return flask.jsonify(retval)


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def start():
    # url = "http://0.0.0.0:5000/"
    # webbrowser.open(url)
    app.run(debug=True, host='0.0.0.0')


def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start()
