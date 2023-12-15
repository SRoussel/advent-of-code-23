"""Advent of code day 15 (part 2)."""

import re
from collections import defaultdict
from functools import reduce


def insert(step, mapping):
    """Insert step into mapping."""
    lens, action = re.split("=|-", step.strip("\n"))
    box = reduce(lambda x, y: ((x + (ord(y))) * 17) % 256, lens, 0)

    if len(action):
        mapping[box][lens] = action
    else:
        mapping[box].pop(lens, None)


def run(filename):
    """Return the sum of lens info."""
    mapping = defaultdict(dict)
    list(map(lambda x: insert(x, mapping), open(filename).read().split(",")))
    def calc(box, pos, focal): return (box + 1) * (pos + 1) * int(focal)
    def inner(box, content): return sum([calc(box, pos, foc) for pos, foc in enumerate(content.values())])
    return sum([inner(box, content) for box, content in mapping.items()])
