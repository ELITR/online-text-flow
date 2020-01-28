#!/usr/bin/env python3

"""Online Text Flow Client"""

__copyright__ = "2020"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


import socketio
import requests
import json
import re
import sys
import click


sio = socketio.Client()

code = {100: "complete", 10: "expected", 1: "incoming"}

opts = {}


@sio.event
def connect():
    print("Connect:", sio.sid, flush=True)


@sio.event
def connect_error():
    print("Error:", sio.sid, flush=True)


@sio.event
def disconnect():
    print()
    print("Disconnect:", sio.sid, flush=True)


def empty(kind='', uniq=1):
    event = {'data': {'text': {"complete": [],
                               "expected": [],
                               "incoming": []}}}
    if kind:
        event['event'] = kind
    event['id'] = uniq
    return event


def post(event, url):
    kind = event['event'] if 'event' in event else ''
    uniq = event['id']
    event['id'] = 'event%s-%d' % ('-' + kind if kind else '', uniq)
    if any(event['data']['text'].values()):
        if opts['-v']:
            resp = requests.post(url + '/post', json=event)
            event['code'] = resp.status_code
            print(json.dumps(event), flush=True)
        else:
            sio.emit('data', event)
            print(".", end="", flush=True)
            sio.sleep(0.01)
        return empty(kind, uniq + 1)
    else:
        return empty(kind, uniq)


def client(kind, url):
    kind = re.sub('\W', '-', " ".join(kind.split()))
    event = empty(kind)
    for line in sys.stdin:
        if line[:1] == "{":
            event = post(event, url)
            event['data'] = json.loads(line)
            event = post(event, url)
        else:
            data = line.split()
            data = [int(data[0]), int(data[1]), " ".join(data[2:])]
            text = event['data']['text']
            text = text["complete"] + text["expected"] + text["incoming"]
            if text and not text[-1][0] < data[0]:
                event = post(event, url)
            event['data']['text'][code[data[1] - data[0]]].append(data)
    post(event, url)
    print(flush=True)


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', default='')
@click.argument('url', default='http://127.0.0.1:5000')
@click.option('-v', '--verbose', is_flag=True, default=False, show_default=True,
              help='Print the JSON event and the response code from the server.')
def main(kind, url, verbose):
    """
    Post data from the standard input as the KIND of events to the URL/post
    endpoint. KIND is empty and URL is http://127.0.0.1:5000 by default.

    If an input line contains two integers as artificial timestamps and then
    some text, an event is being built from the consecutive lines while the
    timestamps increase. The specific difference of timestamps on one line
    classifies the text as "complete", "expected", "incoming", or ignored.

    If the data on a line is a JSON object, the event being built is posted,
    then the data object is decorated and posted as an event of its own.

    Lines that do not fit the logic are ignored. They do not emit the event in
    progress and are printed to the standard error. Use the --verbose option
    to observe the implementation details and the semantics of the events.
    """
    opts['-v'] = verbose
    try:
        sio.connect(url)
        client(kind, url)
        sio.wait()
    except KeyboardInterrupt:
        sys.stderr.close()


if __name__ == '__main__':
    main()
