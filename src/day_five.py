import re
import intervaltree
import math


class MapType:
    def __init__(self):
        self.tree = intervaltree.IntervalTree()
        self.tree[0:math.inf] = 0

    def add(self, dest_start, source_start, length):
        def data_reducer(a, b):
            return dest_start - source_start

        self.tree[source_start:(source_start + length)] = dest_start - source_start
        self.tree.split_overlaps()
        self.tree.merge_equals(data_reducer)

    def convert_tree(self, tree):
        new_tree = intervaltree.IntervalTree()
        for item in tree:
            converted = self.convert_range(item)
            new_tree[converted[0]:converted[1]] = 1
        return new_tree

    def convert_range(self, range):
        return (self.convert(range[0]), self.convert(range[1] - 1) + 1)

    def convert(self, value):
        try:
            return value + sorted(self.tree[value])[0].data
        except IndexError:
            return value


def intersection(a, b):
    splits = (a | b)
    splits.split_overlaps()
    a_int_b = intervaltree.IntervalTree(filter(lambda r: a.overlaps(r) and b.overlaps(r), splits))
    a_int_b.merge_overlaps()
    return a_int_b


def day_five(filename):
    file = open(filename)
    seed_line = []
    mappings = [MapType() for n in range(7)]
    mapping_index = -1

    for line in file:
        line = line.rstrip("\n")
        if "seeds:" in line:
            seed_line.extend([int(char) for char in re.split(r' +', line.strip())[1:]])
        elif ":" in line:
            mapping_index += 1
        elif line != '':
            parsed = [int(char) for char in re.split(r' +', line.strip())]
            mappings[mapping_index].add(parsed[0], parsed[1], parsed[2])

    seeds = intervaltree.IntervalTree()
    for i in range(0, len(seed_line), 2):
        seeds[seed_line[i]:(seed_line[i] + seed_line[i+1])] = 1

    intersections = seeds
    for mapping in mappings:
        intersections = intersection(intersections, mapping.tree)
        intersections = mapping.convert_tree(intersections)

    min = math.inf
    for item in intersections:
        if item[0] < min:
            min = item[0]

    return min
