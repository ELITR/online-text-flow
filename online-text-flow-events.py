#!/usr/bin/env python3

import json
import re
import sys


def event(data, flow=[]):
    if not flow:
        flow = [data]
    else:
        f = len(flow) - 1
        for f in range(f, -1, -1):
            if flow[f][0] < data[0]:
                f += 1
                break
        t = f
        for t in range(t, len(flow)):
            if flow[t][0] >= data[1]:
                t -= 1
                break
        flow = flow[:f] + [data] + flow[t + 1:]
    return flow


def main(kind=''):
    kind = re.sub('\W', '-', " ".join(kind.split()))
    flow = []
    uniq = 0
    for line in sys.stdin:
        try:
            line = " ".join(line.split())
            (f, s, t) = line.split(None, 2)
            data = (int(f), int(s), t)
        except:
            print(line, file=sys.stderr)
        else:
            flow = event(data, flow)
            uniq += 1
            show = {'data': {'flow': flow, 'data': data}}
            if kind:
                show['event'] = kind
                show['id'] = 'event-%s-%d' % (kind, uniq)
            else:
                show['id'] = 'event-%d' % uniq
            print(json.dumps(show), flush=True)


if __name__ == '__main__':
    main(*sys.argv[1:])
