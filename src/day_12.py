"""Advent of code day 12 (part 2)."""

import functools


@functools.lru_cache
def possibilities(str, counts, in_block):
    """Return total number of possibilities for a given string."""
    # Base case: no counts means there should be no damaged springs
    if not counts:
        return "#" not in str

    # Base case: empty string means there should be no record of damages
    if len(str) == 0:
        return sum(counts) == 0

    # First count is zero AKA block is finished
    if counts[0] == 0:
        # There shouldn't be any more damaged springs
        if str[0] == "#":
            return 0

        # Move on to the next block
        return possibilities(str[1:], counts[1:], False)

    # First char is undamaged
    if str[0] == ".":
        # We need to have finished the block to accept undamaged springs
        if in_block:
            return False

        # continue with the same counts
        return possibilities(str[1:], counts, False)

    # First char is damaged
    if str[0] == "#":
        # Continue with the first count decremented
        counts = (counts[0] - 1,) + counts[1:]
        return possibilities(str[1:], counts, True)

    # First char is wildcard; try both undamaged and damaged
    value = 0

    # As before, we can only accept "undamaged" if not in a block
    if not in_block:
        value += possibilities(str[1:], counts, False)

    # As before, "damaged" continues with the first count decremented
    counts = (counts[0] - 1,) + counts[1:]
    value += possibilities(str[1:], counts, True)

    return value


def run(filename):
    """Return the number of points within the loop."""
    file = open(filename)
    total = 0

    for line in file.readlines():
        str, nums = line.strip("\n").split(" ")
        nums = tuple([int(num) for num in nums.split(",")] * 5)
        str = "?".join([str] * 5)
        total += possibilities(str, nums, False)

    return total
