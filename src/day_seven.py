"""Advent of code day 7 (part 2)."""

from collections import Counter
import functools


CardMap = {
    "J": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}


class Rank:
    """Enum for hand ranks."""

    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 2.5
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 3.5
    FOUR_OF_A_KIND = 4
    FIVE_OF_A_KIND = 5


def compare_card(lhs, rhs):
    """Old-style compare function for cards."""
    if CardMap[lhs] < CardMap[rhs]:
        return -1
    elif CardMap[lhs] > CardMap[rhs]:
        return 1

    return 0


def compare_hands(lhs, rhs):
    """Old-style compare function for cards."""
    if lhs[2] < rhs[2]:
        return -1
    elif lhs[2] > rhs[2]:
        return 1

    for l_char, r_char in zip(lhs[0], rhs[0]):
        comp = compare_card(l_char, r_char)

        if comp != 0:
            return comp


def day_seven(filename):
    """Return the total points from the input hands."""
    file = open(filename)

    hands = []

    for line in file:
        split = line.rstrip().split(' ')
        hands.append((split[0], int(split[1])))

    for i, hand in enumerate(hands):
        counter = Counter()
        for char in hand[0].replace("J", ""):
            counter[char] += 1

        rank = Rank.HIGH_CARD
        values = list(counter.values())
        if 5 in values:
            rank = Rank.FIVE_OF_A_KIND
        elif 4 in values:
            rank = Rank.FOUR_OF_A_KIND
        elif 3 in values and 2 in values:
            rank = Rank.FULL_HOUSE
        elif 3 in values:
            rank = Rank.THREE_OF_A_KIND
        elif values.count(2) == 2:
            rank = Rank.TWO_PAIR
        elif 2 in values:
            rank = Rank.ONE_PAIR

        if hand[0].count("J") == 5:
            rank = Rank.FIVE_OF_A_KIND
        else:
            rank += hand[0].count("J")

        hands[i] += rank,

    hands = sorted(hands, key=functools.cmp_to_key(compare_hands))

    sum = 0
    for i, hand in enumerate(hands):
        sum += (i + 1) * hand[1]

    return sum
