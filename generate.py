import json
import random
import sys
from word import Word, WordJSONDecoder


def Terminal(words, orth=None, pos=[], c_form=[]):
    words = list(
        word for word in words if (orth is None or word.orth == orth)
        and word.pos[:len(pos)] == pos and word.c_form[:len(c_form)] == c_form)
    return lambda _depth: random.choice(words)


class NonTerminalBase:
    def get_pron(self):
        return ' '.join(child.get_pron() for child in self.children)

    def __str__(self):
        return ''.join(str(child) for child in self.children)


class NonTerminal(type):
    def __new__(cls, name, f):
        def __init__(self, depth):
            weights, funcs = zip(*f(depth))
            self.children = tuple(
                g(depth + 1)
                for g in random.choices(funcs, weights=weights)[0])

        return type.__new__(cls, name, (NonTerminalBase, ), {
            '__init__': __init__,
        })

    def __init__(*args, **kwargs):
        pass


if __name__ == '__main__':
    words = json.load(sys.stdin, cls=WordJSONDecoder)

    普通名詞 = Terminal(words, pos=['名詞', '普通名詞'])
    連体詞 = Terminal(words, pos=['連体詞'])
    連体形容詞 = Terminal(words, pos=['形容詞'], c_form=['連体形'])
    連体動詞 = Terminal(words, pos=['動詞'], c_form=['連体形'])
    #副詞 = Terminal(words, pos=['副詞'])
    副詞可能名詞 = Terminal(words, pos=['名詞', '普通名詞', '副詞可能'])

    ノ = Terminal(words, orth='の', pos=['助詞', '格助詞'])
    格助詞 = Terminal(words, pos=['助詞', '格助詞'])
    副助詞 = Terminal(words, pos=['助詞', '副助詞'])

    普通名詞節 = NonTerminal(
        '普通名詞節',
        lambda d: [
            (d, (普通名詞, )),
            (1, (ノ格, 普通名詞節)),
            (1, (連体詞, 普通名詞節)),
            (1, (連体形容詞節, 普通名詞節)),
            (1, (連体動詞節, 普通名詞節)),
        ],
    )
    ノ格 = NonTerminal(
        'ノ格',
        lambda d: [
            (1, (普通名詞節, ノ)),
        ],
    )
    連体形容詞節 = NonTerminal(
        '連体形容詞節',
        lambda d: [
            (d, (連体形容詞, )),
            (1, (副詞節, 連体形容詞)),
        ],
    )
    連体動詞節 = NonTerminal(
        '連体動詞節',
        lambda d: [
            (d, (連体動詞, )),
            (1, (副詞節, 連体動詞)),
        ],
    )
    副詞節 = NonTerminal(
        '副詞節',
        lambda d: [
            (d, (副詞類, )),
            (1, (普通名詞節, 副助詞)),
            (1, (普通名詞節, 格助詞)),
            (1, (副詞節, 副詞節)),
        ],
    )
    副詞類 = NonTerminal(
        '副詞類',
        lambda d: [
            #(d, (副詞, )),
            (d, (副詞可能名詞, )),
        ])

    while True:
        result = 普通名詞節(depth=0)
        print(str(result), result.get_pron())
