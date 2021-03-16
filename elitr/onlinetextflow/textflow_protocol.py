def parse(line,types=[int,int]):
    '''get's a line, e.g.
    100 101 The sentence...\n
    returns (100,101), "The sentence...\n"

    types are the types of space-delimited numbers at the beggining of line.
    None for dropping the word.
    '''
    o = ()
    for t in types:
        i = line.index(" ")
        if t is not None:
            n = t(line[:i])
            o += (n,)
        line = line[i+1:]
    return o, line

def brief_to_original(in_stream):
    # converting the brief text-flow into the original one
    buff = {}
    last_f = 0
    last_change = 0
    for line in in_stream:
        (index, status), text = parse(line)
        if index > last_change or index not in buff or buff[index] != line:
            buff[index] = line
            for k in range(last_f+100, index, 100):
                if k in buff:
                    yield buff[k]
            yield line
            if status-index == 100:
                if index in buff:
                    del buff[index]  # so the buffer has constant size
                last_f = index
            last_change = index


def original_to_brief(in_stream):
    buff = {}
    last_ch = 0
    for line in in_stream:
        (index, status), text = parse(line)
        if status-index == 100:
            yield line
            if index in buff:
                del buff[index]
        else:
            if index > last_ch or index not in buff or buff[index] != line:
                yield line
                buff[index] = line
                last_ch = index

class BriefConverter:
    '''Enables using original_to_brief multiple times and hold the state.'''
    def __init__(self):
        self.buff = {}
        self.last_ch = 0

        self.ins_q = []

    def insert_stream(self, stream):
        for s in stream:
            self.insert(s)

    def insert(self, s):
        self.ins_q.append(s)

    def condition(self, line, change_state=False):
        # TODO: repeated code -- ugly :( but easy
        (index, status), text = parse(line)
        if status-index == 100:
            if change_state:
                if index in self.buff:
                    del self.buff[index]
            return True
        if index > self.last_ch or index not in self.buff or self.buff[index] != line:
            if change_state:
                self.buff[index] = line
                self.last_ch = index
            return True
        return False

    def yield_converted(self):
        while self.ins_q:
            line = self.ins_q.pop(0)
            if self.condition(line, change_state=True):
                yield line

    def filter(self):
        out = [ self.condition(line, change_state=True) for line in self.ins_q ]
        self.ins_q = []
        return out
