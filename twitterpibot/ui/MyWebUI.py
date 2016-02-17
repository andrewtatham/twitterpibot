import webbrowser

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def start():
    url = "http://0.0.0.0:5000/"
    webbrowser.open(url)
    app.run(debug=True, host='0.0.0.0')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start()
