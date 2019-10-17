#!/usr/bin/env python3

from flask import json

import flask
import time as sleep

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
    DATA = flask.request.json
    return json.jsonify(DATA)


@app.route('/data')
def data():
    return flask.Response(events(), mimetype="text/event-stream")


@app.route('/')
def home():
    return flask.render_template('index.html', data='/data')


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
    # app.run()
    # app.run(ssl_context='adhoc')
