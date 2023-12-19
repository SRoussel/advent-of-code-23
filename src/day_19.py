"""Advent of code day 19 (part 2)."""

import re

from copy import deepcopy


class ValueInterval:
    """Value interval class."""

    def __init__(self, x, m, a, s):
        """Init."""
        self.x_min = x[0]
        self.x_max = x[1]
        self.m_min = m[0]
        self.m_max = m[1]
        self.a_min = a[0]
        self.a_max = a[1]
        self.s_min = s[0]
        self.s_max = s[1]

    def __repr__(self):
        return f"({self.x_min}, {self.x_max}), ({self.m_min}, {self.m_max}), ({self.a_min}, {self.a_max}), ({self.s_min}, {self.s_max})"


    def contains(self, attr, comp, val):
        min_val = getattr(self, f"{attr}_min")
        max_val = getattr(self, f"{attr}_max")

        if comp == "<":
            return min_val < val
        if comp == ">":
            return max_val > val


    def get(self):
        return (self.x_max + 1 - self.x_min) * (self.m_max + 1 - self.m_min) * (self.a_max + 1 - self.a_min) * (self.s_max + 1 - self.s_min)


    def split(self, attr, comp, val):
        copy = deepcopy(self)

        new_max = val - 1 if comp == "<" else val
        new_min = val + 1 if comp == ">" else val

        setattr(copy, f"{attr}_max", new_max)

        copy2 = deepcopy(self)

        setattr(copy2, f"{attr}_min", new_min)

        return [copy, copy2] if comp == "<" else [copy2, copy]


def parse_condition(value, conds, map, intervals):
    """Parse the given value with the given condition."""
    if type(conds) is not list:
        conds = [conds]

    for cond in conds:
        if cond == "R":
            return False

        if cond == "A":
            intervals.add(value)
            return True

        if ":" in cond:
            check, result = cond.split(":")

            if value.contains(check[0], check[1], int(check[2:])):
                within, without = value.split(check[0], check[1], int(check[2:]))
                parse_condition(within, result, map, intervals)
                value = without
        else:
            return parse_condition(value, map[cond], map, intervals)


def run(filename):
    """Return."""
    func_block, _ = open(filename).read().split("\n\n")

    func_map = {}

    for func in func_block.split("\n"):
        func = re.split(r"\{|\}|\,", func)
        func_map[func[0]] = func[1:-1]

    intervals = set()
    parse_condition(ValueInterval((1, 4000), (1, 4000), (1, 4000), (1, 4000)), func_map["in"], func_map, intervals)
    return sum([interval.get() for interval in intervals])
