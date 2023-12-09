"""Advent of code day 4 (part 2)."""


import collections
import re

global_counter = dict()


def count(index, copies):
    """Return the number of function calls."""
    if index in global_counter:
        return global_counter[index]

    recursions = copies[index]
    total_count = 1

    for call in recursions:
        total_count += count(call, copies)

    global_counter[index] = total_count
    return total_count


def run(filename):
    """Return the total number of scratchcards."""
    file = open(filename)
    lines = []

    for line in file:
        split = re.split(r": | \| ", line.rstrip('\n'))
        winners = re.split(r' +', split[1].strip())
        ours = re.split(r' +', split[2].strip())
        lines.append((winners, ours))

    totals = dict()
    copies = collections.defaultdict(list)

    for index, line in enumerate(lines):
        total = 0
        for n in line[1]:
            if n in line[0]:
                total += 1
        totals[index + 1] = total

    for key, value in totals.items():
        for i in range(key + 1, key + value + 1):
            if i <= len(lines):
                copies[key].append(i)

    return sum([count(n, copies) for n in range(len(lines), 0, -1)])
