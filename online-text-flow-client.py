#!/usr/bin/env python3

import requests
import sys

def main(kind='', url='http://127.0.0.1:5000'):
    for line in sys.stdin:
        try:
            line = " ".join(line.split())
            (f, s, t) = line.split(None, 2)
            data = (int(f), int(s), t)
        except:
            print(line)
        else:
            r = requests.post(url + '/post', json={"data": data, "kind": kind})
            print(r.text)

if __name__ == '__main__':
    main(*sys.argv[1:])
