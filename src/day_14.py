"""Advent of code day 14 (part 2)."""


def tilt(columns):
    """Return columns with rocks shifted north."""
    for item in columns:
        for j in range(1, len(item)):
            if item[j] == "O":
                k = j
                while k > 0 and item[k - 1] == ".":
                    item[k - 1], item[k] = item[k], "."
                    k -= 1
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
        columns = rotate_90(tilt(rotate_90(tilt(rotate_90(tilt(rotate_90(tilt(columns))))))))
        total = sum(len(row) - i for row in columns for i, value in enumerate(row) if value == "O")
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
