#!/usr/bin/env python3

"""Online Text Flow Server"""

__copyright__ = "2019"
__homepage__  = "http://github.com/ELITR/online-text-flow/"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


from flask import json, request, session

import flask
import os

app = flask.Flask(__name__, template_folder=".")

DATA = {'id': ''}


def events():
    uniq = ''
    while True:
        if not uniq == DATA['id']:
            show = 'event: %s\n' % DATA['event'] if 'event' in DATA else ''
            uniq = DATA['id']
            data = json.dumps(DATA['data'])
            yield '%sid: %s\ndata: %s\n\n' % (show, uniq, data)


@app.route('/post', methods=['POST'])
def post():
    global DATA
    DATA = request.json
    return json.jsonify(DATA)


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


@app.route('/')
def index():
    if session.get('auth'):
        return flask.render_template('index.html', data='/data')
    else:
        return flask.redirect('/login')


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(threaded=True, debug=True)
    # app.run(ssl_context='adhoc')
