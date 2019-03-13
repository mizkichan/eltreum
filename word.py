from dataclasses import dataclass
from json import JSONEncoder, JSONDecoder
from typing import Tuple


@dataclass(frozen=True)
class Word:
    surface_form: str
    pos: Tuple[str]
    c_type: Tuple[str]
    c_form: Tuple[str]
    orth_base: str


class WordJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Word):
            return o.__dict__
        return JSONEncoder.default(self, o)


class WordJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            object_hook=object_hook,
            **kwargs,
        )


def object_hook(d):
    try:
        return Word(**d)
    except:
        return d
