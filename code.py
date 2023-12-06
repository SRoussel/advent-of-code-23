import re
import regex
from operator import mul
from functools import reduce
import string
import collections
import intervaltree
import math

def day_one():
    lookup = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    file = open('day_one.txt')
    sum = 0

    for line in file:
        digits = regex.findall(r"\d|zero|one|two|three|four|five|six|seven|eight|nine", line,  overlapped=True)
        first = lookup.get(digits[0], digits[0])
        last = lookup.get(digits[-1], digits[-1])
        sum += int(first + last)

    return sum


def day_two():
    file = open('day_two.txt')
    sum = 0

    for line in file:
        matches = re.findall(r"(\d+) (red|green|blue)", line)
        counts = dict()

        for match in matches:
            if int(match[0]) > counts.get(match[1], 0):
                counts[match[1]] = int(match[0])

        sum += reduce(mul, counts.values(), 1)

    return sum


def seek(values, i, j):
    num_cols = len(values[0])

    list = [values[i][j]]
    starting = j

    k = j - 1
    while k >= 0:
        if values[i][k].isdigit():
            list.insert(0, values[i][k])
            starting = k
        else:
            break
        k = k - 1

    k = j + 1
    while k < num_cols:
        if values[i][k].isdigit():
            list.append(values[i][k])
        else:
            break
        k = k + 1

    return int(''.join(list)), (i, starting)


def get_neighbors(values, i, j):
    num_rows = len(values)
    num_cols = len(values[0])
    neighbors = set()

    if j > 0:
        if values[i][j - 1].isdigit():
            neighbors.add(seek(values, i, j - 1))

    if i < num_rows - 1 and j > 0:
        if values[i + 1][j - 1].isdigit():
            neighbors.add(seek(values, i + 1, j - 1))

    if i > 0 and j > 0:
        if values[i - 1][j - 1].isdigit():
            neighbors.add(seek(values, i - 1, j - 1))

    if i > 0:
        if values[i - 1][j].isdigit():
            neighbors.add(seek(values, i - 1, j))

    if i < num_rows - 1:
        if values[i + 1][j].isdigit():
            neighbors.add(seek(values, i + 1, j))

    if j < num_cols - 1:
        if values[i][j + 1].isdigit():
            neighbors.add(seek(values, i, j + 1))

    if i < num_rows - 1 and j < num_cols - 1:
        if values[i + 1][j + 1].isdigit():
            neighbors.add(seek(values, i + 1, j + 1))

    if i > 0 and j < num_cols - 1:
        if values[i - 1][j + 1].isdigit():
            neighbors.add(seek(values, i - 1, j + 1))

    return neighbors


def day_three():
    file = open('day_three.txt')
    values = [[char for char in line.rstrip('\n')] for line in file]
    sum = 0

    for i, line in enumerate(values):
        for j, char in enumerate(line):
            if char == '*':
                neighbors = get_neighbors(values, i, j)
                if len(neighbors) == 2:
                    neighbors = list(neighbors)
                    sum += neighbors[0][0] * neighbors[1][0]

    return sum


global_counter = dict()


def count(index, copies):
    if index in global_counter:
        return global_counter[index]

    recursions = copies[index]

    total_count = 1

    for call in recursions:
        total_count += count(call, copies)

    global_counter[index] = total_count

    print(total_count)
    return total_count


def day_four():
    file = open('C:/Users/rousselsamuel/desktop/day_four.txt')
    lines = []

    for line in file:
        split = re.split(r": | \| ", line.rstrip('\n'))
        winners = re.split(r' +', split[1].strip())
        ours = re.split(r' +', split[2].strip())
        lines.append((winners, ours))

    totals = dict()
    copies = collections.defaultdict(list)

    for index, line in enumerate(lines):
        total = 0
        for n in line[1]:
            if n in line[0]:
                total += 1
        totals[index + 1] = total

    for key, value in totals.items():
        for i in range(key + 1, key + value + 1):
            if i <= len(lines):
                copies[key].append(i)

    return sum([count(n, copies) for n in range(len(lines), 0, -1)])



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

    def convert_range(self, range):
        return (self.convert(range[0]), self.convert(range[1]))

    def convert(self, value):
        try:
            print(value + sorted(self.tree[value])[0].data)
            return value + sorted(self.tree[value])[0].data
        except IndexError:
            return value


def intersection(a, b):
    splits = (a | b)
    splits.split_overlaps()
    a_int_b = intervaltree.IntervalTree(filter(lambda r: a.overlaps(r) and b.overlaps(r), splits))
    a_int_b.merge_overlaps()
    return a_int_b


def day_five():
    file = open('C:/Users/rousselsamuel/desktop/day_five_mini.txt')
    seed_line = []
    seed_to_soil = MapType()
    soil_to_fertilizer = MapType()
    fertilizer_to_water = MapType()
    water_to_light = MapType()
    light_to_temp = MapType()
    temp_to_humidity = MapType()
    humidity_to_location = MapType()
    data = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temp, temp_to_humidity, humidity_to_location]
    data_index = -1

    for line in file:
        line = line.rstrip("\n")
        if "seeds:" in line:
            seed_line.extend([int(char) for char in re.split(r' +', line.strip())[1:]])
        elif ":" in line:
            data_index += 1
        elif line != '':
            parsed = [int(char) for char in re.split(r' +', line.strip())]
            data[data_index].add(parsed[0], parsed[1], parsed[2])

    min = math.inf
    seeds = []
    tree = intervaltree.IntervalTree()

    for i in range(0, len(seed_line), 2):
        tree[seed_line[i]:(seed_line[i] + seed_line[i+1])] = 1

    total_intersection = tree

    for item in data:
        total_intersection = intersection(total_intersection, item.tree)
        // convert??

    for item in total_intersection:
        print(item)
        seeds.extend([item[0], item[1] - 1])

    for seed in seeds:
        val = humidity_to_location.convert(temp_to_humidity.convert(light_to_temp.convert(water_to_light.convert(fertilizer_to_water.convert(soil_to_fertilizer.convert(seed_to_soil.convert(seed)))))))

        if val < min:
            min = val

    return min


def main():
    print(day_five())


if __name__ == "__main__":
    main()
