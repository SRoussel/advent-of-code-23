"""Advent of code day 17 (part 2)."""

from collections import defaultdict


def add_state(state, cost, grid, visited, queue):
    i, j, di, dj, length = state

    i += di
    j += dj
    length += 1

    if i not in range(0, len(grid)) or j not in range(0, len(grid[0])):
        return None

    cost += int(grid[i][j])

    if i == len(grid) - 1 and j == len(grid[0]) - 1 and length >= 4:
        return cost


    state = (i, j, di, dj, length)

    if state not in visited:
        visited[state] = cost
        queue[cost].append(state)

    return None


def get_cost(grid):
    visited = {}
    queue = defaultdict(list)

    start_right = (0, 0, 0, 1, 0) # i, j, di, dj, len
    start_down = (0, 0, 1, 0, 0)

    add_state(start_right, 0, grid, visited, queue)
    add_state(start_down, 0, grid, visited, queue)

    while len(queue):
        cost = min(queue.keys())
        
        for state in queue.pop(min(queue.keys())):
            i, j, di, dj, length = state

            if length >= 4:
                if result := add_state((i, j, dj, -di, 0), cost, grid, visited, queue):
                    return result

                if result := add_state((i, j, -dj, di, 0), cost, grid, visited, queue):
                    return result

            if length < 10:
                if result := add_state((i, j, di, dj, length), cost, grid, visited, queue):
                    return result


def run(filename):
    """Return the length of the shortest path."""
    grid = [[x for x in line.strip("\n")] for line in open(filename).readlines()]
    return get_cost(grid)
