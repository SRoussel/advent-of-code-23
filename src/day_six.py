import re
from operator import mul
from functools import reduce


def day_six(filename):
    file = open(filename)
    times = [int(char) for char in re.split(r':', file.readline().strip().replace(' ', ''))[1:]]
    distances = [int(char) for char in re.split(r':', file.readline().strip().replace(' ', ''))[1:]]

    result = []

    for time, distance in zip(times, distances):
        winners = []
        for n in range(time):
            if ((time * n) - (n * n) >= distance):
                winners.append(n)
        result.append(len(winners))

    return reduce(mul, result, 1)
