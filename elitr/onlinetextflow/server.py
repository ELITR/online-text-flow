#!/usr/bin/env python3

"""Online Text Flow Server"""

__copyright__ = "2020"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


# https://github.com/singingwolfboy/flask-sse/issues/7
# https://pgjones.gitlab.io/quart/broadcast_tutorial.html
# https://gist.github.com/sebasmagri/a7cede3a708e2365b5a1
# https://stackoverflow.com/questions/27890327/uwsgi-with-gevent-vs-threads


from flask import Flask, json, request, session
from flask_socketio import SocketIO
from gevent import monkey, queue

import flask
import gevent
import os
import click


app = Flask(__name__, template_folder='.')

app.secret_key = os.urandom(16)

url = flask.url_for

sio = SocketIO(app)


DATA = []

OPTS = {'user': 'elitr', 'pass': 'elitr'}

MENU = ['en', 'de', 'cs']


def events():
    stream = queue.Queue()
    try:
        DATA.append(stream)
        while True:
            data = stream.get()
            show = 'event: %s\n' % data['event'] if 'event' in data else ''
            uniq = data['id']
            data = json.dumps(data['data'])
            yield '%sid: %s\ndata: %s\n\n' % (show, uniq, data)
    except:
        DATA.remove(stream)


@sio.on('data')
def emit(data):
    for stream in DATA:
        gevent.spawn(stream.put, data)


@app.route('/stop', methods=['POST'])
def stop():
    for stream in DATA:
        gevent.spawn(stream.put, StopIteration)
    return json.jsonify({"stop": len(DATA)})


@app.route('/post', methods=['POST'])
def post():
    for stream in DATA:
        gevent.spawn(stream.put, request.json)
    return json.jsonify({"post": len(DATA)})


@app.route('/data')
def data():
    return flask.Response(events(), mimetype="text/event-stream")


@app.route("/logout")
def logout():
    session['auth'] = False
    flask.flash('You have been logged out')
    return flask.redirect(url('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['pass'] == OPTS['pass'] and request.form['user'] == OPTS['user']:
            session['auth'] = True
        else:
            flask.flash('The credentials are invalid')
        return flask.redirect(url('index'))
    else:
        return flask.render_template('login.html', login=url('login'))


@app.route('/menu/<path:path>')
def menu(path):
    path = path.replace('/', ' ').split()
    if path:
        session['menu'] = path
    return flask.redirect(url('index'))


@app.route('/menu/')
def reset():
    if 'menu' in session:
        del session['menu']
    return flask.redirect(url('index'))


@app.route('/')
def index():
    if session.get('auth'):
        return flask.render_template('index.html', data=url('data'), menu=session.get('menu', MENU))
    else:
        return flask.redirect(url('login'))


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', nargs=-1)
@click.option('--host', default='127.0.0.1', show_default=True)
@click.option('--port', default=5000, show_default=True)
@click.option('--user', default=OPTS['user'], show_default=True)
@click.option('--pass', default=OPTS['pass'], show_default=True)
@click.option('--debug / --no-debug', default=False, show_default=True)
def main(kind, **opts):
    """
    Run the web app to merge, stream, and display online text flow events.
    Post events at /post and listen to their stream at /data. Browse at /.

    The KIND of events to browse by default is ['en', 'de', 'cs']. Change
    this on the command line for all browsers. Set the /menu endpoint for
    a custom menu in the browser, like /menu/en/de/cs, and empty to reset.

    http://github.com/ELITR/online-text-flow
    """
    global MENU
    if kind:
        MENU = list(kind)
    for key in ['user', 'pass']:
        OPTS[key] = opts[key]
        del opts[key]
    print(' * Opts:', opts)
    print(' * Menu:', MENU)
    monkey.patch_all(ssl=False)
    sio.run(app, **opts)


if __name__ == '__main__':
    main()
