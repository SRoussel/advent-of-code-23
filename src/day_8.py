"""Advent of code day 8 (part 2)."""

import re
import math
import functools


def lcm(a, b):
    """Return least common multiple of a and b."""
    return abs(a * b) // math.gcd(a, b)


def run(filename):
    """Return the number of steps required to reach ZZZ from AAA."""
    file = open(filename)

    steps, nodes = file.read().split('\n\n')

    node_map = dict()

    for node in nodes.splitlines():
        root, left, right, _ = re.split(r"\W+", node)
        node_map[root] = (left, right)

    starting_nodes = [node for node in node_map if node[2] == 'A']

    count = 0
    current_nodes = starting_nodes
    finish_counts = {}

    while len(finish_counts) < len(starting_nodes):
        for step in steps:
            left = step == "L"
            count += 1
            current_nodes = [node_map[node][0 if left else 1] for node in current_nodes]
            for starting, node in zip(starting_nodes, current_nodes):
                if node[2] == 'Z':
                    finish_counts[starting] = count

    return functools.reduce(lcm, finish_counts.values(), 1)
