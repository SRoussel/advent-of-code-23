"""Advent of code day 15 (part 2)."""

import re
from collections import defaultdict
from functools import reduce


def hash(input):
    """Hashing function."""
    return reduce(lambda x, y: ((x + (ord(y))) * 17) % 256, input, 0)


def run(filename):
    """Return the total load after a billion cycles."""
    mapping = defaultdict(dict)

    for step in open(filename).read().split(","):
        values = re.split("=|-", step.strip("\n"))
        box = hash(values[0])

        if len(values[1]):
            mapping[box][values[0]] = values[1]
        else:
            mapping[box].pop(values[0], None)

    total = 0
    for key, value in mapping.items():
        for i, (lens, focal_length) in enumerate(value.items()):
            total += (key + 1) * (i + 1) * int(focal_length)

    return total
