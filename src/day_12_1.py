"""Advent of code day 12 (part 2)."""

import re


def reject(candidate, constraints):
    """Return true if the candidate does not fit the restraints."""
    parts = []
    for constraint in constraints:
        parts.append(r"(?<!#)[\?#]" + f"{{{constraint}}}" + r"(?!#)")

    pattern = r"[\?\.]*".join(parts)
    return None is re.search(pattern, candidate)


def solve(original, constraints, candidate):
    """Use backtracking to count the candidates."""
    if reject(candidate, constraints):
        return 0
    elif "?" not in candidate:
        return candidate.count("#") == sum(constraints)

    current_a = candidate.replace("?", ".", 1)
    current_b = candidate.replace("?", "#", 1)
    return solve(original, constraints, current_a) + solve(original, constraints, current_b)


def run(filename):
    """Return the number of points within the loop."""
    file = open(filename)

    total = 0

    for line in file.readlines():
        str, nums = line.strip("\n").split(" ")
        nums = tuple([int(num) for num in nums.split(",")] * 5)
        str = "?".join([str] * 5)

        print(str)
        total += solve(str, nums, str)

    return total
