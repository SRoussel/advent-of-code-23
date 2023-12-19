"""Advent of code day 18 (part 2)."""


def get_trench_volume(steps):
    """Return the volume of the section defined by steps."""
    current = (0, 0)
    coords = [current]
    boundary_points = 0

    for dir, length in steps:
        x = current[0]
        y = current[1]

        if dir == "3":
            y = current[1] - length
        elif dir == "0":
            x = current[0] + length
        elif dir == "1":
            y = current[1] + length
        elif dir == "2":
            x = current[0] - length

        boundary_points += length
        current = (x, y)
        coords.append(current)

    area = 0.5 * sum([((coords[i][1] + coords[(i + 1) % (len(coords))][1]) *
                       (coords[i][0] - coords[(i + 1) % (len(coords))][0]))
                     for i in range(len(coords))])

    return (boundary_points / 2) + area + 1


def run(filename):
    """Return the volume of the trench."""
    points = []

    for line in [line.rstrip("\n").split(" ") for line in open(filename).readlines()]:
        _, _, color = line
        points.append((color[7:8], int(color[2:7], 16)))

    return int(get_trench_volume(points))
