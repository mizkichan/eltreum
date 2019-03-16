from dataclasses import dataclass
from json import JSONEncoder, JSONDecoder
from typing import Tuple


@dataclass(frozen=True, order=True)
class Word:
    orth: str
    orth_base: str
    pron: str
    pron_base: str
    pos: Tuple[str]
    c_type: Tuple[str]
    c_form: Tuple[str]

    def get_pron(self):
        return self.pron

    def get_phones(self):
        phones = []

        i = 0
        while i < len(self.pron):
            head = self.pron[i:i + 2]
            if head in ('ッー', 'ーッ'):
                raise Exception(self.pron)

            if head in ('キャ', 'キュ', 'キョ', 'ギャ', 'ギュ', 'ギョ', 'シャ', 'シュ', 'シェ',
                        'ショ', 'ジャ', 'ジュ', 'ジェ', 'ジョ', 'チャ', 'チュ', 'チョ', 'ニャ',
                        'ニュ', 'ニョ', 'ヒャ', 'ヒュ', 'ヒョ', 'ビャ', 'ビュ', 'ビョ', 'ピャ',
                        'ピュ', 'ピョ', 'ミャ', 'ミュ', 'ミョ', 'リャ', 'リュ', 'リョ'):
                i += 2
                phones.append(head)
                continue

            head = self.pron[i]
            if head in ('ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ',
                        'ケ', 'ゲ', 'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ', 'ス', 'ズ', 'セ',
                        'ゼ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ッ', 'ツ', 'テ', 'デ', 'ト',
                        'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ',
                        'ピ', 'フ', 'ブ', 'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ',
                        'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ',
                        'ロ', 'ワ', 'ヲ', 'ン', 'ー'):
                i += 1
                phones.append(head)
                continue

            raise Exception(self.pron)

        return phones

    def __str__(self):
        return self.orth


class WordJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Word):
            return vars(o)
        return JSONEncoder.default(self, o)


class WordJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        def object_hook(d):
            try:
                return Word(**d)
            except:
                return d

        super().__init__(
            *args,
            object_hook=object_hook,
            **kwargs,
        )
