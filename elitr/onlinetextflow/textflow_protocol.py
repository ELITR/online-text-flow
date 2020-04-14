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

