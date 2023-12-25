"""Advent of code day 22 (part 2)."""


from collections import defaultdict
from copy import deepcopy


class Point():
    def __init__(self, x, y, z = None):
        self.x = int(x)
        self.y = int(y)
        self.z = None if z is None else int(z)


class Brick():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def max_x(self):
        return max(self.start.x, self.end.x)

    def min_x(self):
        return min(self.start.x, self.end.x)

    def max_y(self):
        return max(self.start.y, self.end.y)

    def min_y(self):
        return min(self.start.y, self.end.y)

    def max_z(self):
        return max(self.start.z, self.end.z)

    def min_z(self):
        return min(self.start.z, self.end.z)

    def is_x_y_point_within(self, point):
        return point.x >= self.min_x() and point.x <= self.max_x() and point.y >= self.min_y() and point.y <= self.max_y()

    def get_x_y_points(self):
        points = set()

        for x in range(self.min_x(), self.max_x() + 1):
            for y in range(self.min_y(), self.max_y() + 1):
                points.add(Point(x, y))

        return points


    def move_down(self, moves):
        self.start.z -= moves
        self.end.z -= moves


    def __eq__(self, other):
        return (self.min_x() == other.min_x() and self.min_y() == other.min_y() and self.min_z() == other.min_z() and 
                self.max_x() == other.max_x() and self.max_y() == other.max_y() and self.max_z() == other.max_z())

    def __hash__(self):
        return hash((self.min_x(), self.max_x(), self.min_y(), self.max_y(), self.min_z(), self.max_z()))


    def __repr__(self):
        return f"({self.start.x}, {self.start.y}, {self.start.z}) - ({self.end.x}, {self.end.y}, {self.end.z})"


def get_descendants(brick, tree):
    if brick not in tree:
        return set()

    children = tree[brick]

    descendants = set()
    descendants.update(children)

    for child in children:
        descendants.update(get_descendants(child, tree))

    return descendants


def run(filename):
    """Return."""
    with open(filename) as file:
        lines = file.readlines()

    z_bottoms = defaultdict(set)
    z_tops = defaultdict(set)

    for i in range(350):
        z_bottoms[i] = set()
        z_tops[i] = set()

    for line in lines:
        start, end = line.rstrip("\n").split("~")
        start_coords = start.split(",")
        end_coords = end.split(",")

        brick = Brick(Point(start_coords[0], start_coords[1], start_coords[2]),
                      Point(end_coords[0], end_coords[1], end_coords[2]))

        z_bottoms[brick.min_z()].add(brick)
        z_tops[brick.max_z()].add(brick)


    to_save = defaultdict(set)
    others = defaultdict(set)

    for z, line in z_bottoms.items():
        to_move = set()

        for brick in line:
            z_brick = z
            hit_bricks = set()
            moves = 0

            while z_brick > 1 and not len(hit_bricks):
                for point in brick.get_x_y_points():
                    for below in z_tops[z_brick - 1]:
                        if below.is_x_y_point_within(point):
                            hit_bricks.add(below)

                if len(hit_bricks):
                    if len(hit_bricks) == 1:
                        to_save[next(iter(hit_bricks))].add(brick)
                    for hit in hit_bricks:
                        others[hit].add(brick)
                    break
                else:
                    moves += 1

                z_brick -= 1

            if moves > 0:
                to_move.add((brick, moves))


        for brick in to_move:
            brick, moves = brick
            z_bottoms[brick.min_z()].remove(brick)
            z_tops[brick.max_z()].remove(brick)
            brick.move_down(moves)
            z_bottoms[brick.min_z()].add(deepcopy(brick))
            z_tops[brick.max_z()].add(deepcopy(brick))
            
        bricks = set()

        for line in z_bottoms.values():
            bricks.update(line)

        for brick in to_save:
            bricks.remove(brick)

    total = 0

    for key in to_save:
        total += len(get_descendants(key, others))

    return total
