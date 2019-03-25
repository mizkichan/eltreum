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
LID = 31  # 正規化すると LID の重複はなくなるので無視してよい
LEMMA_ID = 32

# TODO LID と PRON が同一の語彙をひとつにまとめたい


def process(rows):
    for row in rows:
        if row[POS1] == '感動詞': continue
        if row[POS1] == '空白': continue
        if row[POS1] == '補助記号': continue
        if row[POS1] == '記号': continue
        if row[POS2] == '固有名詞': continue
        if row[GOSHU] == '外': continue
        if row[GOSHU] == '固': continue
        if row[GOSHU] == '記号': continue
        if row[KANA] != row[FORM]: continue
        if row[KANA_BASE] != row[FORM_BASE]: continue
        if any(x in row[PRON]
               for x in ('イュ', 'ウォ', 'ガュ', 'ケュ', 'ゲュ', 'スィ', 'セュ', 'ツァ', 'ティ',
                         'トゥ', 'ネュ', 'フォ', 'ムュ', 'ーッ')):
            continue

        orth = unicodedata.normalize('NFKC', row[ORTH])
        if not is_japanese(orth): continue
        orth_base = unicodedata.normalize('NFKC', row[ORTH_BASE])
        pron = row[PRON]
        pron_base = row[PRON_BASE]

        pos = tuple(x for x in [row[POS1], row[POS2], row[POS3], row[POS4]]
                    if x != '*')
        c_type = tuple(x for x in row[C_TYPE].split('-') if x != '*')
        c_form = tuple(x for x in row[C_FORM].split('-') if x != '*')

        if pos[0] == '形容詞':
            if ((c_form[0] == '終止形' or c_form[0] == '連体形')
                    and pron.endswith('ー') and pron_base.endswith('イ')):
                continue

        if pos[0] in ('連体詞', '接続詞', '助詞', '助動詞'):
            if any(is_kanji(c) for c in orth): continue

        if 0 < len(c_type) and c_type[0].startswith('文語'): continue
        if 1 < len(c_form) and any(x in c_form[1] for x in ('融合', '省略', '音便')):
            continue
        if orth != 'を' and 'を' in orth: continue

        yield Word(orth, orth_base, pron, pron_base, pos, c_type, c_form)


def is_japanese(s):
    return all(is_kanji(c) or is_hiragana(c) for c in s)


def is_kanji(c):
    c = ord(c)
    return (0x4e00 <= c <= 0x9fef  # CJK Unified Ideographs
            or 0x3400 <= c <= 0x4dbf  # CJK Unified Ideographs Extension A
            or 0x20000 <= c <= 0x2a6df  # CJK Unified Ideographs Extension B
            or 0x2a700 <= c <= 0x2b73f  # CJK Unified Ideographs Extension C
            or 0x2b740 <= c <= 0x2b81f  # CJK Unified Ideographs Extension D
            or 0x2b820 <= c <= 0x2ceaf  # CJK Unified Ideographs Extension E
            or 0x2ceb0 <= c <= 0x2ebef  # CJK Unified Ideographs Extension F
            or 0xf900 <= c <= 0xfaff  # CJK Compatibility Ideographs
            or
            0x2f800 <= c <= 0xfa1f  # CJK Compatibility Ideographs Supplement
            )


def is_hiragana(c):
    return (0x3041 <= ord(c) <= 0x308d  # 'あ'-'ろ'
            or c in ('わ', 'を', 'ん'))


if __name__ == '__main__':
    result = list(set(process(csv.reader(sys.stdin))))
    result.sort()
    json.dump(
        result,
        sys.stdout,
        cls=WordJSONEncoder,
        ensure_ascii=False,
        check_circular=False,
        allow_nan=False,
        indent=2,
    )
