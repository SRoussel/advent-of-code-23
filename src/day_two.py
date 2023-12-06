from functools import reduce
from operator import mul
import re


def day_two(filename):
    file = open(filename)
    sum = 0

    for line in file:
        matches = re.findall(r"(\d+) (red|green|blue)", line)
        counts = dict()

        for match in matches:
            if int(match[0]) > counts.get(match[1], 0):
                counts[match[1]] = int(match[0])

        sum += reduce(mul, counts.values(), 1)

    return sum
