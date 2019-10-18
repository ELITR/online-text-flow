#!/usr/bin/env python3

import json
import re
import sys


class Flow():

    def __init__(self):
        self.data = []
        self.drop = []
        self.flow = []
        self.this = -1
        self.sure = 0
        self.crop = 0
        self.text = {"complete": [],
                     "expected": [],
                     "incoming": []}

    def update(self, data):
        self.data = data
        flow = self.flow

        if not flow:
            self.flow = [data]
            self.this = 0
        else:
            f = len(flow) - 1
            for f in range(f, -1, -1):
                if flow[f][1] <= data[0]:
                    f += 1
                    break
            t = f
            for t in range(t, len(flow)):
                if flow[t][1] > data[1]:
                    t -= 1
                    break
            self.flow = flow[:f] + [data] + flow[t + 1:]
            self.drop = flow[f:t + 1]
            self.this = f
            if data[1] <= flow[-1][1]:
                self.sure = f + 1
            if len(self.flow) > f + 1 and self.flow[f + 1][0] < data[1]:
                words = self.flow[f + 1][2].split()
                count = len(data[2].split())
                self.drop.append([self.flow[f + 1][0], data[1], " ".join(words[:count])])
                self.flow[f + 1][0] = data[1]
                self.flow[f + 1][2] = " ".join(words[count:])

        flow = self.flow
        text = {"complete": [], "expected": [], "incoming": []}
        words = []
        self.crop = 0
        for i in range(len(flow)):
            sents = sentences(flow[i][2], words)
            words = sents[-1]
            if len(sents) > 1:
                if i < self.sure:
                    text["complete"].extend(sents[:-1])
                    if words:
                        flow[i][2] = " ".join(words)
                        self.crop = i
                    else:
                        self.crop = i + 1
                else:
                    text["expected"].extend(sents[:-1])
        if words:
            text["incoming"].extend([words])
        self.text = { key: [ " ".join(sent) for sent in text[key] ] for key in text }
        self.flow = flow[self.crop:]
        self.this -= self.crop
        self.sure -= self.crop


def sentences(data, words=[]):
    sents = [words]
    for word in data.split():
        sents[-1].append(word)
        if re.search('\w[.!?]$', word):
            sents.append([])
    return sents


def events(kind='', opts={}):
    kind = re.sub('\W', '-', " ".join(kind.split()))
    flow = Flow()
    uniq = 0
    done = 0
    for line in sys.stdin:
        try:
            line = re.sub('<[^<>]*>', '', line)
            data = line.split()
            data = [int(data[0]), int(data[1]), " ".join(data[2:])]
        except:
            print(line, file=sys.stderr)
        else:
            flow.update(data)
            uniq += 1
            if '-j' in opts:
                show = {'data': {'flow': flow.flow, 'data': flow.data, 'text': flow.text}}
                if kind:
                    show['event'] = kind
                    show['id'] = 'event-%s-%d' % (kind, uniq)
                else:
                    show['id'] = 'event-%d' % uniq
                print(json.dumps(show, sort_keys=True), flush=True)
            elif '-t' in opts:
                if flow.text['complete']:
                    print("\n".join(flow.text['complete']), flush=True)
            else:
                some = 0
                for text in flow.text['complete']:
                    done += 1
                    some += 1
                    print("%d00 %d00 %s" % (some, some + 1, text), flush=True)
                for text in flow.text['expected']:
                    some += 1
                    print("%d00 %d10 %s" % (some, some, text), flush=True)
                for text in flow.text['incoming']:
                    some += 1
                    print("%d00 %d01 %s" % (some, some, text), flush=True)


def main(*args):
    opts = { arg for arg in args if re.search('^-[hjt]$|^--(help|json|text)$', arg) }
    pars = [ arg for arg in args if arg not in opts and not re.search('^-', arg) ]
    opts = { opt[:3][-2:] for opt in opts }
    if '-h' in opts or len(args) > len(opts) + len(pars) or len(pars) > 1:
        print('online-text-flow-events.py [--(help|json|text)] [NAME]', file=sys.stderr)
        print('                            control the output        ', file=sys.stderr)
    else:
        events(pars[0] if pars else '', opts)


if __name__ == '__main__':
    main(*sys.argv[1:])
