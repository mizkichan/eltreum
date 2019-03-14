import json
import random
import sys
from word import Word, WordJSONDecoder


def Terminal(words, surface_form=None, pos=[], c_form=[]):
    words = list(
        word for word in words
        if (surface_form is None or word.surface_form == surface_form)
        and word.pos[:len(pos)] == pos and word.c_form[:len(c_form)] == c_form)
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
    連体詞 = Terminal(words, pos=['連体詞'])
    連体形容詞 = Terminal(words, pos=['形容詞'], c_form=['連体形'])
    連体動詞 = Terminal(words, pos=['動詞'], c_form=['連体形'])
    副詞 = Terminal(words, pos=['副詞'])

    ノ = Terminal(words, surface_form='の', pos=['助詞', '格助詞'])
    格助詞 = Terminal(words, pos=['助詞', '格助詞'])
    副助詞 = Terminal(words, pos=['助詞', '副助詞'])

    名詞節 = NonTerminal(
        '名詞節',
        lambda d: [
            (d, lambda: (名詞(d + 1), )),
            (1, lambda: (ノ格(d + 1), 名詞節(d + 1))),
            (1, lambda: (連体詞(d + 1), 名詞節(d + 1))),
            (1, lambda: (連体形容詞節(d + 1), 名詞節(d + 1))),
            (1, lambda: (連体動詞節(d + 1), 名詞節(d + 1))), ],
    )
    ノ格 = NonTerminal(
        'ノ格',
        lambda d: [
            (1, lambda: (名詞節(d + 1), ノ(d + 1))), ],
    )
    連体形容詞節 = NonTerminal(
        '連体形容詞節',
        lambda d: [
            (d, lambda: (連体形容詞(d + 1), )),
            (1, lambda: (副詞節(d+1), 連体形容詞(d + 1), )),
        ],
    )
    連体動詞節 = NonTerminal(
        '連体動詞節',
        lambda d: [
            (d, lambda: (連体動詞(d + 1), )),
            (1, lambda: (副詞節(d + 1), 連体動詞(d + 1))), ],
    )
    副詞節 = NonTerminal(
        '副詞節',
        lambda d: [
            (d, lambda: (副詞(d + 1), )),
            (1, lambda: (名詞節(d+1), 副助詞(d+1), )),
            (1, lambda: (名詞節(d+1), 格助詞(d+1), )),
        ],
    )

    while True:
        print(str(名詞節(depth=0)))
