import json
import random
import sys
from word import Word, WordJSONDecoder


def Terminal(words, orth=None, pos=[], c_form=[]):
    words = list(
        word for word in words if (orth is None or word.orth == orth)
        and word.pos[:len(pos)] == pos and word.c_form[:len(c_form)] == c_form)
    return lambda _: random.choice(words)


class NonTerminalBase:
    children: tuple

    def get_pron(self):
        return ''.join(child.get_pron() for child in self.children)

    def get_phones(self):
        return sum((child.get_phones() for child in self.children), [])

    def __str__(self):
        return ''.join(str(child) for child in self.children)


def NonTerminal(name, f):
    def __init__(self, depth):
        weights, funcs = zip(*f(depth))
        self.children = tuple(
            g(depth + 1) for g in random.choices(funcs, weights=weights)[0])

    return type(name, (NonTerminalBase, ), {
        '__init__': __init__,
    })


# 連体詞と副詞が使い辛すぎる
if __name__ == '__main__':
    words = json.load(sys.stdin, cls=WordJSONDecoder)

    普通名詞 = Terminal(words, pos=['名詞', '普通名詞'])
    連体詞 = Terminal(words, pos=['連体詞'])
    連体形容詞 = Terminal(words, pos=['形容詞'], c_form=['連体形'])
    連体動詞 = Terminal(words, pos=['動詞'], c_form=['連体形'])
    副詞 = Terminal(words, pos=['副詞'])
    副詞可能名詞 = Terminal(words, pos=['名詞', '普通名詞', '副詞可能'])
    ノ = Terminal(words, orth='の', pos=['助詞', '格助詞'])
    格助詞 = Terminal(words, pos=['助詞', '格助詞'])
    副助詞 = Terminal(words, pos=['助詞', '副助詞'])
    係助詞 = Terminal(words, pos=['助詞', '係助詞'])
    ナ = Terminal(words, orth='な', pos=['助動詞'], c_form=['連体形', '一般'])
    タル = Terminal(words, orth='たる', pos=['助動詞'], c_form=['連体形', '一般'])
    形状詞 = Terminal(words, pos=['形状詞'])
    形状詞可能名詞 = Terminal(words, pos=['名詞', '普通名詞', '形状詞可能'])
    タリ形状詞 = Terminal(words, pos=['形状詞'])

    普通名詞節 = NonTerminal(
        '普通名詞節',
        lambda d: [
            (d, (普通名詞, )),
            (1, (連体節, 普通名詞節)),
        ],
    )
    連体節 = NonTerminal(
        '連体節',
        lambda d: [
            #(d, (連体詞, )),
            (1, (連体格, )),
            (1, (連体形容詞節, )),
            (1, (連体動詞節, )),
            (1, (形状詞類, ナ)),
            (1, (タリ形状詞, タル)),
        ],
    )
    連体格 = NonTerminal(
        '連体格',
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
    形状詞類 = NonTerminal(
        '形状詞類',
        lambda d: [
            (d, (形状詞, )),
            (d, (形状詞可能名詞, )),
        ],
    )
    副詞節 = NonTerminal(
        '副詞節',
        lambda d: [
            #(d, (副詞, )),
            #(d, (副詞可能名詞, )),
            (1, (普通名詞節, 副助詞)),
            (1, (普通名詞節, 格助詞)),
            (1, (普通名詞節, 係助詞)),
            (1, (副詞節, 副詞節)),
        ],
    )

    while True:
        result = 普通名詞節(depth=0)
        if len(result.get_phones()) == 17:
            print(str(result))
