#!/usr/bin/env python3

"""Online Text Flow Client"""

__copyright__ = "2021"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


import websocket
import requests
import json
import re
import sys
import click

from . import textflow_protocol


webs = websocket.WebSocket()

code = {100: "complete", 10: "expected", 1: "incoming"}

opts = {}


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
        if opts['websocket']:
            webs.send(json.dumps(event))
            event['code'] = None
        else:
            resp = requests.post(url + '/post', json=event)
            event['code'] = resp.status_code
        if opts['verbose']:
            print(json.dumps(event), flush=True)
        return empty(kind, uniq + 1)
    else:
        return empty(kind, uniq)

def wrapped_input_stream(in_stream):
    if opts['brief']:
        for line in textflow_protocol.brief_to_original(in_stream):
            yield line
    else:
        for line in in_stream:
            yield line

def client(kind, url):
    if opts['websocket']:
        try:
            webs.connect(url + '/send')
        except:
            url = re.sub('^ws', 'http', url)
            opts['websocket'] = False
    kind = re.sub('\W', '-', " ".join(kind.split()))
    event = empty(kind)
    queue = {
        'complete': {},
        'expected': {},
        'incoming': {}
    }
    for line in wrapped_input_stream(sys.stdin):
        if line[:1] == "{":
            event = post(event, url)
            event['data'] = json.loads(line)
            event = post(event, url)
        else:
            # Until a message is complete, we have to resend it each time we send a message to the server
            data = line.split()
            data = [int(data[0]), int(data[1]), " ".join(data[2:])]
            message_id = int(data[0])
            # Is the incoming message complete, expected or incoming
            bucket = code[data[1] - data[0]]
            # Add/update the message to the appropriate bucket

            # Sometimes the MT does not return anything. If that happens for the complete message, use the last one instead.
            if bucket == "complete" and len(data[2].rstrip()) == 0:
              queue["complete"][message_id] = queue["expected"].pop(message_id, None)
            else:
              queue[bucket][message_id] = data

            if bucket == "expected" or bucket == "complete":
                queue['incoming'].pop(message_id, None)
            if bucket == "complete":
                queue['expected'].pop(message_id, None)

            # Prepare the message to be sent
            for c in queue.keys():
                event["data"]["text"][c] = list(queue[c].values())


            # Send the message to the server
            event = post(event, url)

            # Message marked as complete, no longer needed 
            if bucket == "complete":
                queue['complete'].pop(message_id, None)


    post(event, url)
    if opts['websocket']:
        webs.close()
    print(flush=True)


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', default='')
@click.argument('url', default='ws://127.0.0.1:5000')
@click.option('-v', '--verbose', is_flag=True, default=False, show_default=True,
              help='Print the JSON event and the response code from the server.')
@click.option('-b', '--brief', is_flag=True, default=False, show_default=True,
              help='Input is converted from the "brief" text flow to the '
              'original "verbose" protocol with repeated sentences.')
def main(kind, url, verbose, brief):
    """
    Emit data as the KIND of events to the URL/send websocket or the URL/post
    endpoint, depending on the scheme of the URL. Consider websockets over
    recurring requests. KIND is '' and URL is ws://127.0.0.1:5000 by default.

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
    opts['websocket'] = url.split(':')[0] in ['ws', 'wss']
    if not opts['websocket']:
        print('Consider using %s/send websockets instead of %s/post requests :)'
              % (url.replace('http', 'ws', 1), url), file=sys.stderr)
    opts['verbose'] = verbose
    opts['brief'] = brief
    try:
        client(kind, url)
    except KeyboardInterrupt:
        sys.stderr.close()


if __name__ == '__main__':
    main()
