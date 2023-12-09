"""Advent of code day 9 (part 2)."""


def extrapolate(sequence, backward=False):
    """Return the next value in the sequence."""
    if all([n == 0 for n in sequence]):
        return 0

    differences = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]

    return (sequence[0] - extrapolate(differences, True)) if backward else (
        sequence[-1] + extrapolate(differences))


def day_nine(filename):
    """Return the number of steps required to reach ZZZ from AAA."""
    file = open(filename)
    sequences = [[int(num) for num in line.split()] for line in file.readlines()]
    extrapolates = [extrapolate(sequence, True) for sequence in sequences]
    return sum(extrapolates)
