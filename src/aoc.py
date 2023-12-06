import sys
import day_one
import day_two
import day_three
import day_four
import day_five
import day_six


days = [day_one.day_one, day_two.day_two, day_three.day_three, day_four.day_four, day_five.day_five, day_six.day_six]


def main():
    day = int(sys.argv[1])
    print(days[day - 1](f"inputs/day_{day}.txt"))


if __name__ == "__main__":
    main()
