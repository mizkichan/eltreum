import json
import random
import sys
from word import Word, WordJSONDecoder


def Terminal(words, pos=[], c_form=[]):
    words = list(
        word for word in words
        if word.pos[:len(pos)] == pos and word.c_form[:len(c_form)] == c_form)
    return lambda _depth: random.choice(words)


class NonTerminal(type):
    def __new__(cls, name, f):
        def __init__(self, depth):
            weights, funcs = zip(*f(depth))
            self.children = random.choices(funcs, weights=weights)[0]()

        def __str__(self):
            return ''.join(str(child) for child in self.children)

        return type.__new__(cls, name, (object, ), {
            '__init__': __init__,
            '__str__': __str__
        })

    def __init__(*args, **kwargs):
        pass


if __name__ == '__main__':
    words = json.load(sys.stdin, cls=WordJSONDecoder)

    名詞 = Terminal(words, pos=['名詞'])
    連体形形容詞 = Terminal(words, pos=['形容詞'], c_form=['連体形'])
    連体形動詞 = Terminal(words, pos=['動詞'], c_form=['連体形'])
    連体詞 = Terminal(words, pos=['連体詞'])

    名詞節 = NonTerminal(
        '名詞節',
        lambda d: [
            (d, lambda: (名詞(d + 1), )),
            (1, lambda: (ノ格(d + 1), 名詞節(d + 1))),
            (1, lambda: (連体形形容詞(d + 1), 名詞節(d + 1))),
            (1, lambda: (連体詞(d + 1), 名詞節(d + 1))),
            (1, lambda: (連体節(d + 1), 名詞節(d + 1))), ],
    )
    ノ格 = NonTerminal(
        'ノ格',
        lambda d: [
            (1, lambda: (名詞節(d + 1), Word('の', ('助詞', '格助詞'), (), (), 'の'))), ],
    )
    連体節 = NonTerminal(
        '連体節',
        lambda d: [
            (d, lambda: (連体形動詞(d + 1), )), ],
    )

    while True:
        print(str(名詞節(depth=0)))
