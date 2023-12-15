"""Advent of code day 2 (part 2)."""


from functools import reduce
from operator import mul
import re


def line_product(line):
    """Return the product of the values in the line."""
    counts = dict()
    for num, color in re.findall(r"(\d+) (red|green|blue)", line):
        if int(num) > counts.get(color, 0):
            counts[color] = int(num)

    return reduce(mul, counts.values(), 1)


def run(filename):
    """Return the sum of the powers of each game."""
    return sum([line_product(line) for line in open(filename).readlines()])
