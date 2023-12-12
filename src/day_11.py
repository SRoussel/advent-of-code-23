"""Advent of code day 11 (part 2)."""


def get_between(lhs, rhs, universe):
    """Get the values between lhs and rhs."""
    betweens = []

    if lhs[0] > rhs[0]:
        for i in range(rhs[0] + 1, lhs[0]):
            betweens.append(universe[i][rhs[1]])
    elif rhs[0] > lhs[0]:
        for i in range(lhs[0] + 1, rhs[0]):
            betweens.append(universe[i][lhs[1]])

    if lhs[1] > rhs[1]:
        for i in range(rhs[1] + 1, lhs[1]):
            betweens.append(universe[rhs[0]][i])
    elif rhs[1] > lhs[1]:
        for i in range(lhs[1] + 1, rhs[1]):
            betweens.append(universe[lhs[0]][i])

    return betweens


def run(filename):
    """Return the number of points within the loop."""
    file = open(filename)

    universe = []
    for line in file.readlines():
        line = line.strip("\n")

        if "#" not in line:
            universe.append(["!"] * len(line))
        else:
            universe.append([*line])

    indices = []

    for j in range(len(universe[0])):
        double = True
        for i in range(len(universe)):
            if universe[i][j] == "#":
                double = False
                break

        if double:
            indices.append(j)

    indices.reverse()

    for index in indices:
        for i in range(len(universe)):
            universe[i][index] = "!"

    galaxies = []

    for i in range(len(universe)):
        for j in range(len(universe[0])):
            if universe[i][j] == "#":
                galaxies.append((i, j))

    distances = {}

    for lhs in galaxies:
        for rhs in galaxies:
            key = frozenset({lhs, rhs})
            if len(key) == 2:
                expandeds = get_between(lhs, rhs, universe).count("!")
                distances[key] = abs(rhs[0] - lhs[0]) + abs(rhs[1] - lhs[1])
                distances[key] += (1000000 - 1) * expandeds

    return sum(distances.values())
