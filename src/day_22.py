"""Advent of code day 22 (part 2)."""


from collections import defaultdict
from copy import deepcopy

class Point():
    def __init__(self, x, y, z = None):
        self.x = int(x)
        self.y = int(y)
        self.z = None if z is None else int(z)


class Brick():
    def __init__(self, id, start, end):
        self.id = id
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
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


    def __repr__(self):
        return f"({self.id} {self.start.x}, {self.start.y}, {self.start.z}) - ({self.end.x}, {self.end.y}, {self.end.z})"


def populate_space_from_filename(filename):
    with open(filename) as file:
        lines = file.readlines()

    z_bottoms = defaultdict(set)
    z_tops = defaultdict(set)

    for i in range(350):
        z_bottoms[i] = set()
        z_tops[i] = set()

    global_brick_id = 0

    for line in lines:
        start, end = line.rstrip("\n").split("~")
        start_coords = start.split(",")
        end_coords = end.split(",")

        brick = Brick(global_brick_id, Point(start_coords[0], start_coords[1], start_coords[2]),
                      Point(end_coords[0], end_coords[1], end_coords[2]))

        z_bottoms[brick.min_z()].add(brick)
        z_tops[brick.max_z()].add(brick)

        global_brick_id += 1

    return z_bottoms, z_tops


def count_fallen(key, child_tree, parent_tree):
    fallen = set()
    fallen.add(key)
    children = child_tree[key]

    while len(children):
        copy = deepcopy(children)
        for child in copy:
            supported = False
            parents = parent_tree[child]

            for parent in parents:
                if parent != key and parent not in fallen:
                    supported = True

            if not supported:
                fallen.add(child)
            
            children.remove(child)
            if child in child_tree:
                children.update(child_tree[child])

    return len(fallen) - 1


def move_blocks_down(z_tops, z_bottoms):
    child_tree = defaultdict(set)
    parent_tree = defaultdict(set)

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
                    for hit in hit_bricks:
                        child_tree[hit].add(brick)
                        parent_tree[brick].add(hit)
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
    
    return child_tree, parent_tree


def move_blocks_down(z_bottoms, z_tops):    
    child_tree = defaultdict(set)
    parent_tree = defaultdict(set)

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
                    for hit in hit_bricks:
                        child_tree[hit].add(brick)
                        parent_tree[brick].add(hit)
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

    return child_tree, parent_tree


def run(filename):
    """Return."""
    child_tree, parent_tree = move_blocks_down(*populate_space_from_filename(filename))

    return sum([count_fallen(child, child_tree, parent_tree) for child in child_tree])
