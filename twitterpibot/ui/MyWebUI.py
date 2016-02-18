import webbrowser

import flask

from twitterpibot import identities

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/status')
@app.route('/status/<screen_name>')
def status(screen_name=None):
    retval = [
        {
            "screen_name": i.screen_name,
            "url": "status/" + i.screen_name,
        } for i in identities.all_identities
        if screen_name is None or screen_name == i.screen_name
        ]

    return flask.jsonify(result=retval)


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def start():
    url = "http://0.0.0.0:5000/"
    webbrowser.open(url)
    app.run(debug=True, host='0.0.0.0')


def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start()
