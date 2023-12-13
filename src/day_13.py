"""Advent of code day 13 (part 2)."""


def get_mirror_helper(block, type, original=None):
    """Return the index of the mirror for the given block."""
    indices = []
    for i in range(len(block) - 1):
        if block[i] == block[i + 1]:
            indices.append(i)

    filtered = indices.copy()
    for index in indices:
        i = index
        j = index + 1

        while i >= 0 and j < len(block):
            if block[i] != block[j]:
                filtered.remove(index)
                break

            i -= 1
            j += 1

    if len(filtered) == 0:
        return None

    if len(filtered) == 1:
        return filtered[0], type

    for item in filtered:
        if item != original[0] or type != original[1]:
            return item, type

    # shouldn't reach this
    return filtered


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


def run(filename):
    """Return the sum of mirror indices after weighting."""
    file = open(filename)

    blocks = file.read().split("\n\n")

    for i, block in enumerate(blocks):
        blocks[i] = [[char for char in line] for line in block.split("\n")]

    total = 0

    for count, block in enumerate(blocks):
        mirror = get_mirror(block)
        original = mirror

        for i in range(len(block)):
            for j in range(len(block[0])):
                flip(block, i, j)
                alt_mirror = get_mirror(block, original)

                if alt_mirror is not None:
                    mirror = alt_mirror

                flip(block, i, j)

        total += ((mirror[0] + 1) * 100) if (mirror[1] == "H") else (mirror[0] + 1)

    return total
