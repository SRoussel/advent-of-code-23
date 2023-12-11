"""Advent of code day 10 (part 2)."""


types = ["-", "|","L", "J", "7", "F"]


def bounds_check(values, num_rows, num_cols):
    return [value for value in values if value[0] >= 0 and value[0] < num_rows and value[1] >= 0 and value[1] < num_cols]


def connects_to(values, i, j, seed=None):
    value = values[i][j] if seed == None else seed
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
    for i in range(len(values)):
        for j in range(len(values[0])):
            if values[i][j] == "S":
                return (i, j)
    
    return (-1, -1)


loop = []


def traverse(start, values):
    loop.append(start)
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

    return steps


def run(filename):
    file = open(filename)
    values = [[char for char in line.rstrip('\n')] for line in file]
    
    start = find_start(values)
    first_connections = []

    for type in types:
        first_connections = connects_to(values, *start, type)

        if len(first_connections) == 2:
            values[start[0]][start[1]] = type
            break
    
    traverse(start, values)
    print(loop)
    return 0
