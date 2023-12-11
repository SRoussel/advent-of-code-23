"""Advent of code day 10 (part 2)."""


types = ["-", "|", "L", "J", "7", "F"]


def bounds_check(points, num_rows, num_cols):
    """Return a bounds checked version of points."""
    return [point for point in points if
            point[0] >= 0 and point[0] < num_rows and
            point[1] >= 0 and point[1] < num_cols]


def connects_to(values, i, j, seed=None):
    """Return a list of all points connected to (i, j)."""
    value = values[i][j] if seed is None else seed
    num_rows = len(values)
    num_cols = len(values[0])

    if value == "-":
        return bounds_check([(i, j - 1), (i, j + 1)], num_rows, num_cols)
    elif value == "|":
        return bounds_check([(i - 1, j), (i + 1, j)], num_rows, num_cols)
    elif value == "L":
        return bounds_check([(i - 1, j), (i, j + 1)], num_rows, num_cols)
    elif value == "J":
        return bounds_check([(i - 1, j), (i, j - 1)], num_rows, num_cols)
    elif value == "7":
        return bounds_check([(i, j - 1), (i + 1, j)], num_rows, num_cols)
    elif value == "F":
        return bounds_check([(i, j + 1), (i + 1, j)], num_rows, num_cols)
    else:
        return []


def find_start(values):
    """Return the start point."""
    for i in range(len(values)):
        for j in range(len(values[0])):
            if values[i][j] == "S":
                return (i, j)
    return (-1, -1)


def traverse(start, values):
    """Traverse the loop, returning the distance of the furthest point."""
    loop = [start]
    left, right = connects_to(values, start[0], start[1])
    left_previous = start
    right_previous = start
    steps = 1
    while left != right:
        loop.append(left)
        loop.insert(0, right)
        left_neighbors = connects_to(values, left[0], left[1])
        right_neighbors = connects_to(values, right[0], right[1])
        left_neighbors.remove(left_previous)
        right_neighbors.remove(right_previous)
        left_previous = left
        right_previous = right
        left = left_neighbors[0]
        right = right_neighbors[0]
        steps += 1

    loop.append(left)
    return steps, loop


def run(filename):
    """Return the number of points within the loop."""
    file = open(filename)
    values = [[char for char in line.rstrip('\n')] for line in file]

    start = find_start(values)
    first_connections = []

    for type in types:
        first_connections = connects_to(values, *start, type)

        if len(first_connections) == 2:
            values[start[0]][start[1]] = type
            break

    steps, loop = traverse(start, values)

    inside = 0
    for i in range(len(values)):
        not_in_loop = [(i, j) for j in range(len(values[0])) if (i, j) not in loop]
        in_loop = [(i, j) for j in range(len(values[0])) if (i, j) in loop]

        for point in not_in_loop:
            ray = "".join([values[n[0]][n[1]] for n in in_loop if values[n[0]][n[1]] != "-" and n[1] > point[1]])
            inside += 1 == (ray.count("|") + ray.count("L7") + ray.count("FJ")) % 2

    return inside
