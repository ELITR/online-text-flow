#!/usr/bin/env python3

"""Online Text Flow Server"""

__copyright__ = "2019"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


# https://github.com/singingwolfboy/flask-sse/issues/7
# https://pgjones.gitlab.io/quart/broadcast_tutorial.html


from flask import json, request, session

import flask
import os
import queue
import click


app = flask.Flask(__name__, template_folder='.')

app.secret_key = os.urandom(16)

DATA = []

SHOW = ['en', 'de', 'cs']


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


@app.route('/post', methods=['POST'])
def post():
    for stream in DATA:
        stream.put(request.json)
    return json.jsonify({})


@app.route('/data')
def data():
    return flask.Response(events(), mimetype="text/event-stream")


@app.route("/logout")
def logout():
    session['auth'] = False
    flask.flash('You have been logged out')
    return flask.redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['pass'] == 'elitr' and request.form['user'] == 'elitr':
            session['auth'] = True
        else:
            flask.flash('The credentials are invalid')
        return flask.redirect('/')
    else:
        return flask.render_template('login.html')


@app.route('/show/<path:path>')
def show(path):
    path = path.replace('/', ' ').split()
    if path:
        session['show'] = path
    return flask.redirect('/')


@app.route('/show/')
def reset():
    if 'show' in session:
        del session['show']
    return flask.redirect('/')


@app.route('/')
def index():
    if session.get('auth'):
        return flask.render_template('index.html', data='/data', show=session.get('show', SHOW))
    else:
        return flask.redirect('/login')


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', nargs=-1)
@click.option('--host', default='127.0.0.1', show_default=True)
@click.option('--port', default=5000, show_default=True)
@click.option('--debug / --no-debug', default=False, show_default=True)
@click.option('--threaded / --no-threaded', default=True, show_default=True)
@click.option('--ssl_context', default=None, show_default=True,
              help='Secure with HTTPS if needed.  [TEXT: adhoc]')
def main(kind, **opts):
    """
    Run the web app to merge, stream, and display online text flow events.
    Post events at /post and listen to their stream at /data. Browse at /.

    http://github.com/ELITR/online-text-flow
    """
    global SHOW
    if kind:
        SHOW = list(kind)
    print(' * Opts:', opts)
    print(' * Show:', SHOW)
    app.run(**opts)


if __name__ == '__main__':
    main()
