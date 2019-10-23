#!/usr/bin/env python3

"""Online Text Flow Client"""

__copyright__ = "2019"
__homepage__  = "http://github.com/ELITR/online-text-flow/"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


import requests
import json
import re
import sys


key = {100: "complete", 10: "expected", 1: "incoming"}


def empty(kind='', uniq=1):
    event = {'data': {'flow': [],
                      'data': [],
                      'text': {"complete": [],
                               "expected": [],
                               "incoming": []}}}
    if kind:
        event['event'] = kind
    event['id'] = uniq
    return event


def post(event, url):
    kind = event['event'] if 'event' in event else ''
    uniq = event['id']
    if isinstance(uniq, str):
        uniq = int(re.search('-([0-9]+)$', uniq).group(1))
    else:
        event['id'] = 'event%s-%d' % ('-' + kind if kind else '', uniq)
    if any(event['data']['text'].values()):
        reply = requests.post(url + '/post', json=event)
        # print(reply.text)
        return empty(kind, uniq + 1)
    else:
        return empty(kind, uniq)


def main(kind='', url='http://127.0.0.1:5000'):
    kind = re.sub('\W', '-', " ".join(kind.split()))
    event = empty(kind)
    for line in sys.stdin:
        try:
            if line[:1] == "{":
                event = post(event, url)
                post(json.loads(line), url)
            else:
                data = line.split()
                data = [int(data[0]), int(data[1]), " ".join(data[2:])]
                text = event['data']['text']
                text = text["complete"] + text["expected"] + text["incoming"]
                if text and not text[-1][0] < data[0]:
                    event = post(event, url)
                event['data']['text'][key[data[1] - data[0]]].append(data)
        except:
            print(line, file=sys.stderr)
    post(event, url)


if __name__ == '__main__':
    main(*sys.argv[1:])
