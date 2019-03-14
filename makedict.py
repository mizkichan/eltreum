import csv
import json
import sys
import unicodedata
from word import Word, WordJSONEncoder

SURFACE_FORM = 0
LEFT_CONTEXT_ID = 1
RIGHT_CONTEXT_ID = 2
COST = 3

# 品詞
POS1 = 4
POS2 = 5
POS3 = 6
POS4 = 7

C_TYPE = 8  # 活用形
C_FORM = 9  # 活用型
L_FORM = 10  # 語彙素読み
LEMMA = 11  # 語彙素
ORTH = 12  # 書字形出現形
PRON = 13  # 発音形出現形
ORTH_BASE = 14  # 書字形基本形
PRON_BASE = 15  # 発音形基本形
GOSHU = 16  # 語種

# 結合情報
I_TYPE = 17
I_FORM = 18
F_TYPE = 19
F_FORM = 20
I_CON_TYPE = 21
F_CON_TYPE = 22

TYPE = 23  # 類
KANA = 24  # 仮名形出現形
KANA_BASE = 25  # 仮名形基本形
FORM = 26  # 語形出現形
FORM_BASE = 27  # 語形基本形

# アクセント情報
A_TYPE = 28
A_CON_TYPE = 29
A_MOD_TYPE = 30

# ID
LID = 31
LEMMA_ID = 32


def process(rows):
    for row in rows:
        if row[POS1] == '感動詞': continue
        if row[POS1] == '空白': continue
        if row[POS1] == '補助記号': continue
        if row[POS1] == '記号': continue
        if row[POS2] == '固有名詞': continue
        if row[C_TYPE].startswith('文語'): continue
        if row[GOSHU] == '外': continue
        if row[GOSHU] == '固': continue
        if row[GOSHU] == '記号': continue
        if row[KANA] != row[FORM]: continue

        orth = unicodedata.normalize('NFKC', row[ORTH])
        if not is_japanese(orth): continue
        orth_base = unicodedata.normalize('NFKC', row[ORTH_BASE])
        pron = row[PRON]
        pron_base = row[PRON_BASE]

        pos = tuple(x for x in [row[POS1], row[POS2], row[POS3], row[POS4]]
                    if x != '*')
        c_type = tuple(x for x in row[C_TYPE].split('-') if x != '*')
        c_form = tuple(x for x in row[C_FORM].split('-') if x != '*')

        if (pos[0] == '形容詞' and (c_form[0] == '終止形' or c_form[0] == '連体形')
                and row[PRON].endswith('ー') and row[PRON_BASE].endswith('イ')):
            continue
        if (pos[0] == '動詞' and (c_form[0] == '終止形' or c_form[0] == '連体形')
                and c_form[1] == '撥音便'):
            continue

        yield Word(orth, orth_base, pron, pron_base, pos, c_type, c_form)


def is_japanese(s):
    return all(is_kanji(c) or is_hiragana(c) for c in s)


def is_kanji(c):
    return 0x4e00 <= ord(c) <= 0x9fff or 0xf900 <= ord(c) <= 0xfaff


def is_hiragana(c):
    return 0x3040 <= ord(c) <= 0x309f


if __name__ == '__main__':
    json.dump(
        list(set(process(csv.reader(sys.stdin)))),
        sys.stdout,
        cls=WordJSONEncoder,
        ensure_ascii=False,
        check_circular=False,
        allow_nan=False,
        indent=2,
    )
