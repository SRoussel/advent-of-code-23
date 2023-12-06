"""Advent of code day 3 (part 2)."""


def seek(values, i, j):
    """Get the number including (i, j)."""
    num_cols = len(values[0])

    list = [values[i][j]]
    starting = j

    k = j - 1
    while k >= 0:
        if values[i][k].isdigit():
            list.insert(0, values[i][k])
            starting = k
        else:
            break
        k = k - 1

    k = j + 1
    while k < num_cols:
        if values[i][k].isdigit():
            list.append(values[i][k])
        else:
            break
        k = k + 1

    return int(''.join(list)), (i, starting)


def get_neighbors(values, i, j):
    """Return the indices neighboring (i, j) in values."""
    num_rows = len(values)
    num_cols = len(values[0])
    neighbors = set()

    if j > 0:
        if values[i][j - 1].isdigit():
            neighbors.add(seek(values, i, j - 1))

    if i < num_rows - 1 and j > 0:
        if values[i + 1][j - 1].isdigit():
            neighbors.add(seek(values, i + 1, j - 1))

    if i > 0 and j > 0:
        if values[i - 1][j - 1].isdigit():
            neighbors.add(seek(values, i - 1, j - 1))

    if i > 0:
        if values[i - 1][j].isdigit():
            neighbors.add(seek(values, i - 1, j))

    if i < num_rows - 1:
        if values[i + 1][j].isdigit():
            neighbors.add(seek(values, i + 1, j))

    if j < num_cols - 1:
        if values[i][j + 1].isdigit():
            neighbors.add(seek(values, i, j + 1))

    if i < num_rows - 1 and j < num_cols - 1:
        if values[i + 1][j + 1].isdigit():
            neighbors.add(seek(values, i + 1, j + 1))

    if i > 0 and j < num_cols - 1:
        if values[i - 1][j + 1].isdigit():
            neighbors.add(seek(values, i - 1, j + 1))

    return neighbors


def day_three(filename):
    """Return the sum of the gear ratios."""
    file = open(filename)
    values = [[char for char in line.rstrip('\n')] for line in file]
    sum = 0

    for i, line in enumerate(values):
        for j, char in enumerate(line):
            if char == '*':
                neighbors = get_neighbors(values, i, j)
                if len(neighbors) == 2:
                    neighbors = list(neighbors)
                    sum += neighbors[0][0] * neighbors[1][0]

    return sum
