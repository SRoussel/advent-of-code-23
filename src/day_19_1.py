"""Advent of code day 19 (part 1)."""

import re


class Value:
    """Value class."""

    def __init__(self, x, m, a, s):
        """Init."""
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def sum(self):
        """Return the sum of value's attributes."""
        return self.x + self.m + self.a + self.s

    def __repr__(self):
        return f"({self.x}, {self.m}, {self.a}, {self.s})"


def parse_condition(value, conds, map):
    """Parse the given value with the given condition."""
    if type(conds) is not list:
        conds = [conds]

    print(value, conds)

    for cond in conds:
        if cond == "R":
            return False

        if cond == "A":
            return True

        if ":" in cond:
            check, result = cond.split(":")
            val = getattr(value, check[0])

            if check[1] == ">" and val > int(check[2:]):
                return parse_condition(value, result, map)

            elif check[1] == "<" and val < int(check[2:]):
                return parse_condition(value, result, map)
        else:
            return parse_condition(value, map[cond], map)


def run(filename):
    """Return."""
    func_block, values_block = open(filename).read().split("\n\n")

    func_map = {}

    for func in func_block.split("\n"):
        func = re.split(r"\{|\}|\,", func)
        func_map[func[0]] = func[1:-1]

    total = 0
    for value in values_block.split("\n"):
        x, m, a, s = re.findall(r"\d+", value)

        value = Value(x, m, a, s)

        if parse_condition(value, func_map["in"], func_map):
            total += value.sum()

    return total
