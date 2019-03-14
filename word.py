from dataclasses import dataclass
from json import JSONEncoder, JSONDecoder
from typing import Tuple


@dataclass(frozen=True)
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
