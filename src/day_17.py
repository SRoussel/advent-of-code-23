"""Advent of code day 17 (part 2)."""

import math


# node = (i, j, dir, len)

class Dir:
    North = 0
    East = 1
    South = 2
    West = 3

class Node:
    def __init__(self, i, j, dir, len):
        self.i = i
        self.j = j
        self.dir = dir
        self.len = len

def generate_nodes(node, grid):
    if (nodelen < 3):



def run(filename):
    """Return the length of the shortest path."""
    grid = [[x for x in line.strip("\n")] for line in open(filename).readlines()]
    return len(grid)

