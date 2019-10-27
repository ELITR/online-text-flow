#!/usr/bin/env python3

"""Online Text Flow Events"""

__copyright__ = "2019"
__homepage__  = "http://github.com/ELITR/online-text-flow/"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


import json
import re
import sys
import click


code = {"complete": 100, "expected": 10, "incoming": 1}

opts = {}


class Flow():

    def __init__(self):
        self.data = []
        self.drop = []
        self.flow = []
        self.this = -1
        self.sure = 0
        self.crop = 0
        self.done = 0
        self.text = empty()

    def update(self, data):
        self.data = data
        self.__flow__()
        self.__text__()

    def __flow__(self):
        data = self.data
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
                minus = sum(len(drop[2].split()) for drop in self.drop)
                if count > minus:
                    self.drop.append([self.flow[f + 1][0], data[1],
                                      " ".join(words[:count - minus])])
                    self.flow[f + 1][0] = data[1]
                    self.flow[f + 1][2] = " ".join(words[count - minus:])

    def __text__(self):
        flow = self.flow
        text = empty()
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
        done = self.done
        text["complete"] = enumerated(text, "complete", done)
        done += len(text["complete"])
        self.done = done
        text["expected"] = enumerated(text, "expected", done)
        done += len(text["expected"])
        text["incoming"] = enumerated(text, "incoming", done)
        self.text = text
        self.flow = flow[self.crop:]
        self.this -= self.crop
        self.sure -= self.crop


def empty():
    return {"complete": [], "expected": [], "incoming": []}


def enumerated(text, key, done):
    return [ [i * 100, i * 100 + code[key], " ".join(t)]
             for (i, t) in enumerate(text[key], done + 1) ]


def sentences(data, words=[]):
    sents = [words]
    for word in data.split():
        sents[-1].append(word)
        if re.search('\w[.!?]$', word):
            sents.append([])
    return sents


def events(kind=''):
    kind = re.sub('\W', '-', " ".join(kind.split()))
    flow = Flow()
    uniq = 0
    for line in sys.stdin:
        try:
            line = re.sub('<[^<>]*>', '', line)
            data = line.split()
            data = [int(data[0]), int(data[1]), " ".join(data[2:])]
        except:
            print(line, file=sys.stderr)
        else:
            flow.update(data)
            if opts['-t']:
                if flow.text["complete"]:
                    print("\n".join(t for [i, j, t] in flow.text["complete"]), flush=True)
            elif opts['-j']:
                uniq += 1
                show = {'data': {'flow': flow.flow, 'data': flow.data, 'text': flow.text}}
                if kind:
                    show['event'] = kind
                    show['id'] = 'event-%s-%d' % (kind, uniq)
                else:
                    show['id'] = 'event-%d' % uniq
                print(json.dumps(show, sort_keys=True), flush=True)
            else:
                for key in ["complete", "expected", "incoming"]:
                    for [i, j, t] in flow.text[key]:
                        print("%d %d %s" % (i, j, t), flush=True)
    if opts['-t']:
        print("".join("\n" + t for [i, j, t] in flow.text["expected"]), flush=True)
        print("".join("\n" + t for [i, j, t] in flow.text["incoming"]), flush=True)


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', default='')
@click.option('-j', '--json', is_flag=True, default=False, show_default=True,
              help='Output JSON objects with detailed information, unless the --text option is used.')
@click.option('-t', '--text', is_flag=True, default=False, show_default=True,
              help='Output the resulting "complete", "expected", "incoming" text, delimited by blank lines.')
def main(kind, json, text):
    """
    Turn data from ASR into text for NMT. Events are classified sentences
    rather than text chunks evolving in time and disturbing the flow.

    If not empty, KIND is used to name the events being emitted in the JSON
    format. The KIND is empty by default.
    """
    opts['-j'] = json
    opts['-t'] = text
    try:
        events(kind)
    except BrokenPipeError:
        sys.stderr.close()


if __name__ == '__main__':
    main()
