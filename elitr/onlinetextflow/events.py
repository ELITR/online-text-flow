#!/usr/bin/env python3

"""Online Text Flow Events"""

__copyright__ = "2020"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


import json
import re
import sys
import click

from mosestokenizer import MosesSentenceSplitter

from elitr.onlinetextflow import textflow_protocol

code = {"complete": 100, "expected": 10, "incoming": 1}

opts = {}


class Flow():

    def __init__(self, timestamps=False, lang="en"):
        self.data = []
        self.drop = []
        self.flow = []
        self.this = -1
        self.sure = 0
        self.crop = 0
        self.done = 0
        self.text = empty()
        self.timestamps = timestamps
        self.splitter = MosesSentenceSplitter(lang)

    def update(self, data):
        self.data = data
        self.__flow__()
        self.__text__()

    def __flow__(self):
        data = self.data.copy()
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
            if data[0] >= flow[-1][1]:
                self.sure = f
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
        w_beg = -1  # beginning timestamp of words
        self.crop = 0
        for i in range(len(flow)):
            sents, w_beg = self._timestamped_sentences(*flow[i], words, w_beg)
            words = sents[-1][::]
            if self.timestamps:
                words[0] = words[0].split()[-1]
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
            text["incoming"].extend([sents[-1]])
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


    def _sentences(self, data, words=[]):
        '''language-dependent sentence splitting
        by MosesSentenceSplitter
        '''
        to_split = []
        w = " ".join(words)
        if w:
            to_split.append(w)
        if data:
            to_split.append(data)
        if to_split:
            return [ s.split() for s in self.splitter(to_split) ]
        return []

    def _timestamped_sentences(self, beg, end, data, words=[], w_beg=-1):
        '''returns: sentences as a list of lists of tokens, beginning
        timestamps of the last "sentence" (or a sentence prefix)

        if self.timestamps:
            the first "token" of each sentence is actually "beg end token",
        else:
            it's not

        The sentence-timestamps are estimated from the beginning and ending
        timestamps of the whole segment, by the sentence lengths in characters. 

        DISCLAIMER: They may be inaccurate, if the speech pace varies!!!
        '''
        sents = self._sentences(data, words)
        if not self.timestamps:
            return sents, -1

        if words:
            beg = w_beg
        s_lens = [sum(len(w)+1 for w in s) for s in sents]  # sentence len in chars, including spaces (+1)
        c_len = sum(s_lens)  # total len in chars
        b = beg
        out_sents = []
        last_b = b
        for l,s in zip(s_lens,sents):
            e = b+(l/c_len)*(end-beg)
            s[0] = "%1.1f %1.1f %s" % (b,e,s[0])  # "beg end token"
            out_sents.append(s)
            last_b = b
            b = e
        return out_sents, last_b

def empty():
    return {"complete": [], "expected": [], "incoming": []}


def enumerated(text, key, done):
    return [ [i * 100, i * 100 + code[key], " ".join(t)]
             for (i, t) in enumerate(text[key], done + 1) ]


def bug_fix_repetitions(in_stream):
    # by Dominik
    # bad hack to fix https://github.com/ELITR/online-text-flow/issues/5
    # TODO: fix permanently and remove
    last = None
    i = 0
    for line in in_stream:
        (beg, end), line = textflow_protocol.parse(line, types=[int, int])
        if last and (beg,end) == last:
            i += 1
        else:
            i = 0
        last = (beg,end)
        yield "%d %d %s\n" % (beg*10, end*10+i, line)



def yield_events(in_stream, timestamps=False, lang="en"):
    flow = Flow(timestamps, lang)
    show = []
    for line in bug_fix_repetitions(in_stream):
        try:
            line = re.sub('<[^<>]*>', ' ', line)
            data = line.split()
            data = [int(data[0]), int(data[1]), " ".join(data[2:])]
        except:
            print(line, file=sys.stderr, flush=True)
        else:
            flow.update(data)
            if '-t' in opts:
                for [i, j, t] in flow.text["complete"]:
                    yield t
            elif '-j' in opts:
                d = flow.__dict__.copy()
                del d['splitter']
                j = json.dumps(d, sort_keys=True)
                yield j
            else:
                text = []
                for key in ["complete", "expected", "incoming"]:
                    for [i, j, t] in flow.text[key]:
                        text.append("%d %d %s" % (i, j, t))
                if len(show) < len(text) or not show[-len(text):] == text:
                    show = text
                    for ijt in text:
                        yield ijt
    if '-t' in opts:
        for key in ["expected", "incoming"]:
            yield ''
            for [i, j, t] in flow.text[key]:
                yield t

def events(in_stream=sys.stdin, brief=False, timestamps=False, lang="en"):
    if brief:
        wrap = textflow_protocol.original_to_brief
    else:
        wrap = lambda x: x
    for line in wrap(yield_events(in_stream, timestamps, lang)):
        print(line,flush=True)

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('lang', default='en')
@click.option('-l', '--line', 'mode', flag_value='-l', default='--line', show_default=True,
              help='Output the events as lines of artificial timestamps and text, '
              'where specific differences in timestamps group the events and '
              'classify the text as "complete", "expected", and "incoming".')
@click.option('-j', '--json', 'mode', flag_value='-j',
              help='Output the events as JSON objects with detailed information '
              'about the data, the flow, the text, and other indicators.')
@click.option('-t', '--text', 'mode', flag_value='-t',
              help='Output the resulting text split into classes by empty lines.')
@click.option('--timestamps', 'timestamps',is_flag=True, default=False, show_default=True,
              help='Output the real events timestamps as the 3rd and 4th '
	      'space-separated column. The timestamps are approximated '
	      'from the input segments by length in characters.')
@click.option('-b', '--brief', is_flag=True, default=False, show_default=True,
              help='Input is converted from the "brief" text flow to the '
              'original "verbose" protocol with repeated sentences.')
def main(lang, mode, timestamps, brief):
    """
    Turn data from speech recognition into text for machine translation. The
    emitted events are classified sentences rather than text chunks evolving
    in time and disturbing the flow. The complete text is emitted just once.

    LANG is the language code passed to MosesSentenceSplitter, 'en' if none.
    """
    opts[mode] = mode
    try:
        events(sys.stdin, brief, timestamps, lang)
    except KeyboardInterrupt:
        sys.stderr.close()


if __name__ == '__main__':
    main()
