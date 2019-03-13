import json
import random
import sys
from word import Word, WordJSONDecoder

_名詞 = None
_連体形形容詞 = None
_連体形動詞 = None
_連体詞 = None


def 名詞節(words, d):
    return random.choices(
        [
            lambda: 名詞(words, d + 1),
            lambda: ノ格(words, d + 1) + 名詞節(words, d + 1),
            lambda: 連体形形容詞(words, d + 1) + 名詞節(words, d + 1),
            lambda: 連体詞(words, d + 1) + 名詞節(words, d + 1),
            lambda: 連体節(words, d + 1) + 名詞節(words, d + 1),
        ],
        weights=[d, 1, 1, 1, 1],
    )[0]()


def 名詞(words, d):
    global _名詞
    if _名詞 is None:
        _名詞 = [word for word in words if word.pos[0] == '名詞']
    return (random.choice(_名詞), )


def 連体形形容詞(words, d):
    global _連体形形容詞
    if _連体形形容詞 is None:
        _連体形形容詞 = [
            word for word in words
            if word.pos[0] == '形容詞' and word.c_form[0] == '連体形'
        ]
    return (random.choice(_連体形形容詞), )


def 連体形動詞(words, d):
    global _連体形動詞
    if _連体形動詞 is None:
        _連体形動詞 = [
            word for word in words
            if word.pos[0] == '動詞' and word.c_form[0] == '連体形'
        ]
    return (random.choice(_連体形動詞), )


def 連体詞(words, d):
    global _連体詞
    if _連体詞 is None:
        _連体詞 = [word for word in words if word.pos[0] == '連体詞']
    return (random.choice(_連体詞), )


def ノ格(words, d):
    return 名詞節(words, d + 1) + (Word('の', ('助詞', '格助詞'), (), (), 'の'), )


def 連体節(words, d):
    return random.choices(
        [
            lambda: 連体形動詞(words, d + 1),
        ],
        weights=[d],
    )[0]()


if __name__ == '__main__':
    words = json.load(sys.stdin, cls=WordJSONDecoder)
    while True:
        print(''.join(word.surface_form for word in 名詞節(words, 0)))
