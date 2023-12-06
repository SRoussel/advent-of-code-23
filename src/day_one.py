import regex


def day_one(filename):
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

    re_string = r"\d|zero|one|two|three|four|five|six|seven|eight|nine"

    file = open(filename)
    sum = 0

    for line in file:
        digits = regex.findall(re_string, line,  overlapped=True)
        first = lookup.get(digits[0], digits[0])
        last = lookup.get(digits[-1], digits[-1])
        sum += int(first + last)

    return sum
