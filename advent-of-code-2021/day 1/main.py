"""Advent of Code 2021 Day 1."""


def main(file_input='input.txt'):
    depths = [int(number) for number in get_file_contents(file_input)]
    number_of_increases = count_increases(depths)
    print(number_of_increases)
    increases_in_window = count_increases_in_window(depths)
    print(increases_in_window)


def count_increases_in_window(numbers, window_length=3):
    """Count number of times sum of the window with window_length increases."""
    increases = 0
    for index, _ in enumerate(numbers[:-window_length]):
        prev_window = sum(numbers[index:index + window_length])
        cur_window = sum(numbers[index + 1:index + window_length + 1])
        if cur_window > prev_window:
            increases += 1
    return increases


def count_increases(numbers):
    """Count number of times value in numbers increases."""
    increases = 0
    for prev_index, number in enumerate(numbers[1:]):
        if number > numbers[prev_index]:
            increases += 1
    return increases


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
