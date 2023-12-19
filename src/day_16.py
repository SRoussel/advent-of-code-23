"""Advent of code day 16 (part 2)."""

import copy


class Beam:
    class Dir:
        North = 0
        East = 1
        South = 2
        West = 3

    def __init__(self, i, j, dir, grid, coords, visited):
        self.i = i
        self.j = j
        self.dir = dir
        self.grid = grid
        self.coords = coords
        self.visited = visited
        if self.valid():
            self.visited.add((i, j, dir))
            self.coords.add((i, j))

    def advance(self):
        if Beam.Dir.North == self.dir:
            self.i -= 1

        elif Beam.Dir.East == self.dir:
            self.j += 1

        elif Beam.Dir.South == self.dir:
            self.i += 1

        elif Beam.Dir.West == self.dir:
            self.j -= 1

        if self.valid() and (self.i, self.j, self.dir) not in self.visited:
            self.visited.add((self.i, self.j, self.dir))
            self.coords.add((self.i, self.j))
        else:
            self.i = -1
            self.j = -1

    def valid(self):
        return (self.i >= 0 and self.j >= 0 and
                self.i < len(self.grid) and self.j < len(self.grid[0]))

    def process(self):
        self.advance()

        if self.valid():
            step = self.grid[self.i][self.j]

            if step == "-":
                if self.dir == Beam.Dir.North or self.dir == Beam.Dir.South:
                    self.dir = Beam.Dir.East
                    new_beam = Beam(self.i, self.j, Beam.Dir.West, self.grid, self.coords, self.visited)
                    return new_beam
            elif step == "|":
                if self.dir == Beam.Dir.East or self.dir == Beam.Dir.West:
                    self.dir = Beam.Dir.North
                    new_beam = Beam(self.i, self.j, Beam.Dir.South, self.grid, self.coords, self.visited)
                    return new_beam
            elif step == "/":
                if self.dir == Beam.Dir.North:
                    self.dir = Beam.Dir.East
                elif self.dir == Beam.Dir.East:
                    self.dir = Beam.Dir.North
                elif self.dir == Beam.Dir.South:
                    self.dir = Beam.Dir.West
                elif self.dir == Beam.Dir.West:
                    self.dir = Beam.Dir.South
            elif step == "\\":
                if self.dir == Beam.Dir.North:
                    self.dir = Beam.Dir.West
                elif self.dir == Beam.Dir.East:
                    self.dir = Beam.Dir.South
                elif self.dir == Beam.Dir.South:
                    self.dir = Beam.Dir.East
                elif self.dir == Beam.Dir.West:
                    self.dir = Beam.Dir.North

        return None


    def __repr__(self) -> str:
        return f"({self.i}, {self.j}), {self.dir}"

def propogate(beams):
    while len(beams):
        beam = beams.pop()
        child = beam.process()
        if beam.valid():
            beams.append(beam)
        if child and child.valid():
            beams.append(child)


def try_start(i, j, dir, grid):
    grid = copy.deepcopy(grid)
    coords = set()
    visited = set()
    beam = Beam(i, j, dir, grid, coords, visited)
    propogate([beam])

    for i, j in coords:
        grid[i][j] = "#"

    return len(coords)


def run(filename):
    """Return the number of energized squares."""
    grid = [[x for x in line.strip("\n")] for line in open(filename).readlines()]

    possible_starts = [(x, -1, Beam.Dir.East) for x in range(len(grid))]
    possible_starts.extend([(x, len(grid[0]), Beam.Dir.West) for x in range(len(grid))])
    possible_starts.extend([(-1, x, Beam.Dir.South) for x in range(len(grid[0]))])
    possible_starts.extend([(len(grid), x, Beam.Dir.North) for x in range(len(grid[0]))])

    return max([try_start(*x, grid) for x in possible_starts])

