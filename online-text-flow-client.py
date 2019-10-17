#!/usr/bin/env python3

import requests
import json
import sys

def main(url='http://127.0.0.1:5000'):
    for line in sys.stdin:
        try:
            event = json.loads(line)
        except:
            print(line)
        else:
            reply = requests.post(url + '/post', json=event)
            print(reply.text)

if __name__ == '__main__':
    main(*sys.argv[1:])
