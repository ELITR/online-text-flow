# originally from SimulStreaming/translate

import regex
from functools import lru_cache
class SentenceSegmenter:

    """
    Regex sentence splitter for Latin languages, Japanese and Chinese.
    It is based on sacrebleu TokenizerV14International(BaseTokenizer).
    
    Returns: a list of strings, where each string is a sentence.
    Spaces following punctuation are appended after punctuation within the sequence.
    Total number of characters in the output is the same as in the input.  
    """

    sep = 'ŽžŽžSentenceSeparatorŽžŽž'  # string that certainly won't be in src or target
    latin_terminals = '!?.'
    jap_zh_terminals = '。！？'
    terminals = latin_terminals + jap_zh_terminals

    def __init__(self):
        # end of sentence characters:
        terminals = self.terminals
        self._re = [
            # Separate out punctuations preceeded by a non-digit. 
            # If followed by space-like sequence of characters, they are 
            # appended to the punctuation, not to the next sequence.
            (regex.compile(r'(\P{N})(['+terminals+r'])(\p{Z}*)'), r'\1\2\3'+self.sep),
            # Separate out punctuations followed by a non-digit
            (regex.compile(r'('+terminals+r')(\P{N})'), r'\1'+self.sep+r'\2'),
#            # Separate out symbols
            # -> no, we don't tokenize but segment the punctuation
#            (regex.compile(r'(\p{S})'), r' \1 '),
        ]

    @lru_cache(maxsize=2**16)
    def __call__(self, line):
        for (_re, repl) in self._re:
            line = _re.sub(repl, line)
        return [ t for t in line.split(self.sep) if t != '' ]

if __name__ == "__main__":
	s = SentenceSegmenter()
	t = "首が折れますよ。あなたがそれを組織するなんて信じられません、ええ。本当に、私は、疲弊していると思います。そのような複雑なイベント、私が聞くと、4、5台のカメラがあって、その範囲を想像できませぬ、つまり、それらの人々が私をどれほど好きなのか、例えば、ある種のプロセスのように思えるはずなので、私はそれを地面に置きます。さて、地面に置きましょう、少なくとも100人くらいはいるでしょう。少なくとも100人。あなたが言っているのは、少なくとも200人、300,000人くらいだと思うのですが。少なくとも14日間、集中的に働くこと、つまり実際にはイベント全体を確実にするための生産、そしてそれを技術的に組織するための努力、そして、私は知らない、効果的な、それに加えて、全体を組織し、時間割、計画、脚本を整理する必要があ"
	x = s(t)
	print(x)

	y = 'þŽŘÝþ首が折れ þŽŘÝþますよ。あなたがそれを þŽŘÝþ組織するなんて信じられません þŽŘÝþ、 þŽŘÝþええ þŽŘÝþ。本当に þŽŘÝþ、私は、疲弊していると思います。 þŽŘÝþそのような複雑なイベント、 þŽŘÝþ私が þŽŘÝþ聞くと、4、5台のカメラがあ þŽŘÝþって、 þŽŘÝþその範囲を想像できませ þŽŘÝþぬ、つまり、 þŽŘÝþそれらの人々が私をどれほど好きなのか、 þŽŘÝþ例えば、 þŽŘÝþある種のプロセスのように思えるはずなので、 þŽŘÝþ私はそれを地面に置 þŽŘÝþきます。さて、地面に置きましょう、少なくとも100人くらいはいるでしょう þŽŘÝþ。 þŽŘÝþ少なくとも100人。あなたが言っているのは、少なくとも200人、300,000人くらいだと思うのですが。少なくとも14日間、集中的に働くこと、つまり実際にはイベント全体を確実にするための生産、そしてそれを技術的に組織するための努力、そして þŽŘÝþ、私は知らない、効果的な、それに加えて、全体を組織し、 þŽŘÝþ時間割、 þŽŘÝþ計画、脚本を整理する þŽŘÝþ必要があ þŽŘÝþって、そのために、まずは、現実の種類、それは重要ではない。あなたが知っているように、これはおそらく今'
	print(s(y))
