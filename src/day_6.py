"""Advent of code day 6 (part 2)."""


import re
from operator import mul
from functools import reduce


def run(filename):
    """Return the product of the number of ways each record can be beaten."""
    file = open(filename)
    times = [int(char) for char in re.split(r':', file.readline().strip().replace(' ', ''))[1:]]
    distances = [int(char) for char in re.split(r':', file.readline().strip().replace(' ', ''))[1:]]

    result = []

    for time, distance in zip(times, distances):
        winners = []
        for n in range(time):
            if ((time * n) - (n * n) >= distance):
                winners.append(n)
        result.append(len(winners))

    return reduce(mul, result, 1)
