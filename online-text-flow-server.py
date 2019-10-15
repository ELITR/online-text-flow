#!/usr/bin/env python3

from flask import json

import flask
import datetime
import time as sleep
import re

app = flask.Flask(__name__, template_folder=".")

DATA = []
FLOW = {}


def eventsData():
    where = 0
    while True:
        if len(DATA) > where:
            kind = DATA[where]['kind']
            if kind:
                show = 'event: %s\n' % kind
                uniq = 'data-%s-%d' % (kind, where + 1)
            else:
                show = ''
                uniq = 'data-%d' % (where + 1)
            data = json.dumps(DATA[where])
            yield '%sid: %s\ndata: %s\n\n' % (show, uniq, data)
            where += 1
        else:
            sleep.sleep(1)


def eventsFlow():
    where = {}
    while True:
        for kind in FLOW:
            if kind not in where:
                where[kind] = 0
            if len(FLOW[kind]) > where[kind]:
                if kind:
                    show = 'event: %s\n' % kind
                    uniq = 'flow-%s-%d' % (kind, where[kind] + 1)
                else:
                    show = ''
                    uniq = 'flow-%d' % (where[kind] + 1)
                data = FLOW[kind][where[kind]]
                data = ",\ndata:  ".join([ json.dumps(line) for line in data ])
                yield '%sid: %s\ndata: [%s]\n\n' % (show, uniq, data)
                where[kind] += 1


def updateData(data):
    DATA.append(data)


def updateFlow(data):
    kind = data['kind']
    line = data['data']
    if kind not in FLOW:
        FLOW[kind] = [[line]]
    else:
        flow = FLOW[kind][-1]
        f = len(flow) - 1
        for f in range(f, -1, -1):
            if flow[f][0] < line[0]:
                f += 1
                break
        t = f
        for t in range(t, len(flow)):
            if flow[t][0] >= line[1]:
                t -= 1
                break
        flow = flow[:f] + [line] + flow[t + 1:]
        FLOW[kind].append(flow)


@app.route('/stat')
def stat():
    if len(DATA):
        return "Date: %s\nTime: %s\nSize: %s\n" % (DATA[-1]['date'], DATA[-1]['time'], len(DATA))
    else:
        return ""


@app.route('/dump')
def dump():
    return json.jsonify({'DATA': DATA, 'FLOW': FLOW})


@app.route('/remove/<kind>')
def clear(kind):
    global DATA
    size = len(DATA)
    DATA = [ line for line in DATA if line['kind'] != kind ]
    del FLOW[kind]
    return json.jsonify({'kind': kind, 'size': len(DATA) - size})


@app.route('/post', methods=['POST'])
def post():
    data = flask.request.json
    user = flask.session.get('user', 'anonymous')
    when = datetime.datetime.now().replace(microsecond=0)
    time = when.time()
    date = when.date()
    kind = " ".join(data['kind'].split())
    kind = re.sub('\W', '-', kind)
    updateData({"time": time.isoformat(),
                "date": date.isoformat(),
                "user": user,
                "data": data['data'],
                "kind": kind})
    updateFlow(DATA[-1])
    return json.jsonify(DATA[-1])


@app.route('/data')
def data():
    return flask.Response(eventsData(), mimetype="text/event-stream")


@app.route('/flow')
def flow():
    return flask.Response(eventsFlow(), mimetype="text/event-stream")


@app.route('/')
def home():
    (en, cs) = [ "no events in the '%s' stream yet" % k for k in ["en", "cs"] ]
    return flask.render_template('index.html', text={"en": en, "cs": cs})


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
    # app.run()
    # app.run(ssl_context='adhoc')
