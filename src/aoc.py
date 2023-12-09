"""Advent of code 2023."""

import sys


def main():
    """Run advent of code."""
    day_n = f"day_{int(sys.argv[1])}"
    day_func = getattr(__import__(day_n), 'run')
    print(day_func(f"inputs/{day_n}.txt"))


if __name__ == "__main__":
    main()
