"""Advent of code day 23 (part 2)."""

from collections import defaultdict
from copy import deepcopy

import functools

import networkx


def is_walkable(char):
    return char != '#'

def get_neighbors(values, i, j, path):
    """Return the indices neighboring (i, j) in values."""
    num_rows = len(values)
    num_cols = len(values[0])
    neighbors = set()

    char = values[i][j]

    if j > 0 and is_walkable(values[i][j - 1]):
            neighbors.add((i, j - 1))

    if i > 0 and is_walkable(values[i - 1][j]):
            neighbors.add((i - 1, j))

    if i < num_rows - 1 and is_walkable(values[i + 1][j]):
            neighbors.add((i + 1, j))

    if j < num_cols - 1 and is_walkable(values[i][j + 1]):
            neighbors.add((i, j + 1))

    for previous in path:
        if previous in neighbors:
            neighbors.remove(previous)

    return neighbors

@functools.lru_cache
def longest_path_length(position, map):
    pass

def run(filename):
    """Return."""
    with open(filename) as file:
        values = [[char for char in line.rstrip('\n')] for line in file]

    for j, char in enumerate(values[0]):
        if char == '.':
            start = (0, j)
            break

    for j, char in enumerate(values[len(values) - 1]):
        if char == '.':
            end = (len(values) - 1, j)
            break

    stack = [(start, [], -1, start)]

    iterations = 0
    completions = []
    junction_length_map = defaultdict(set)
    global_path = []
    while len(stack):
        new = []
        for position, path, distance, last_junction in stack:
            distance += 1
            if position == end:
                completions.append(iterations)
                junction_length_map[last_junction].add((position, distance))
                path.remove(last_junction)
                global_path += path
            else:
                neighbors = get_neighbors(values, *position, path + global_path)

                if len(neighbors) > 1 or position in junction_length_map:
                    junction_length_map[last_junction].add((position, distance))
                    junction_length_map[position].add((last_junction, distance))
                    path.remove(last_junction)
                    last_junction = position
                    distance = 0
                    global_path += path
                    path = []

                for neighbor in neighbors:
                    new.append((neighbor, path + [position], distance, last_junction))

        iterations += 1 if len(new) else 0
        stack = new

    nodes = [(start, 0, [])]

    iterations = 0
    test_completions = []
    while len(nodes):
        new = []
        for position, distance, path in nodes:
            if position in junction_length_map:
                for new_position, new_distance in junction_length_map[position]:
                    if new_position not in path:
                        new.append((new_position, distance + new_distance, path + [position]))
            elif position == end:
                test_completions.append(distance)

        nodes = new

    return max(test_completions)

