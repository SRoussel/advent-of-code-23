"""Advent of code day 13 (part 2)."""


def filter(i, block):
    """Return True if i is a valid index."""
    j = i + 1

    while i >= 0 and j < len(block):
        if block[i] != block[j]:
            return False

        i -= 1
        j += 1

    return True


def get_mirror_helper(block, type, original=None):
    """Return the index of the mirror for the given block."""
    indices = [i for i in range(len(block) - 1) if filter(i, block)]

    if len(indices) == 0:
        return None

    if len(indices) == 1:
        return indices[0], type

    for item in indices:
        if item != original[0] or type != original[1]:
            return item, type

    return indices  # Shouldn't be reached


def get_mirror(block, original=None):
    """Return the index of the mirror for the given block, trying both normal and transpose."""
    mirror = get_mirror_helper(block, "H", original)

    if mirror is None or mirror == original:
        transpose = [[row[i] for row in block] for i in range(len(block[0]))]
        mirror = get_mirror_helper(transpose, "V", original)

    return mirror if mirror != original else None


def flip(block, i, j):
    """Flip the value at the given index."""
    block[i][j] = "." if block[i][j] == "#" else "#"


def block_value(block):
    """Return the value of the block."""
    mirror = get_mirror(block)
    original = mirror

    for i in range(len(block)):
        for j in range(len(block[0])):
            flip(block, i, j)
            alt_mirror = get_mirror(block, original)
            mirror = alt_mirror if alt_mirror is not None else mirror
            flip(block, i, j)

    return ((mirror[0] + 1) * 100) if (mirror[1] == "H") else (mirror[0] + 1)


def run(filename):
    """Return the sum of mirror indices after weighting."""
    f = open(filename)
    blocks = [[[x for x in row] for row in block.split("\n")] for block in f.read().split("\n\n")]
    return sum([block_value(block) for block in blocks])
