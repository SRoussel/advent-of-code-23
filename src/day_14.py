"""Advent of code day 14 (part 2)."""


def tilt(columns):
    """Return columns with rocks shifted north."""
    for i in range(len(columns)):
        for j in range(len(columns[0])):
            if "O" == columns[i][j]:
                k = j - 1
                m = j
                while k >= 0:
                    if columns[i][k] == ".":
                        columns[i][k] = "O"
                        columns[i][m] = "."
                        m = k
                        k -= 1
                    else:
                        break
    return columns


def rotate_90(columns):
    """Rotate columns 90 degrees counter-clockwise."""
    return list([list(item) for item in zip(*columns)])[::-1]


def get_load(columns, index):
    """Return the load of columns after index + 1 cycles."""
    states = {}
    totals = {}
    count = 0

    while True:
        columns = tilt(columns)
        columns = tilt(rotate_90(columns))
        columns = tilt(rotate_90(columns))
        columns = tilt(rotate_90(columns))
        columns = rotate_90(columns)

        total = 0
        for i in range(len(columns)):
            for j in range(len(columns[0])):
                if "O" == columns[i][j]:
                    total += len(columns[0]) - j

        str = "".join(item for col in columns for item in col)
        if str in states:
            return totals[states[str] + ((index - states[str]) % (count - states[str]))]

        states[str] = count
        totals[count] = total
        count += 1


def run(filename):
    """Return the total load after a billion cycles."""
    file = open(filename)

    lines = [line.rstrip("\n") for line in file.readlines()]
    columns = [[row[i] for row in lines] for i in range(len(lines[0]))]
    return get_load(columns, 999999999)
