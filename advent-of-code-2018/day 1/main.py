"""Advent of Code 2018 Day 1."""


def main(file_input='input.txt'):
    frequency_changes = [int(line.strip())
                         for line in get_file_contents(file_input)]
    print(f'Resulting frequency: {sum(frequency_changes)}')
    repeated = find_repeated_frequency(frequency_changes)
    print(f'First repeated frequency: {repeated}')


def find_repeated_frequency(changes):
    """Find first frequency that's reached twice."""
    cur_frequency = 0
    seen = set()
    while True:
        for change in changes:
            if cur_frequency in seen:
                return cur_frequency
            seen.add(cur_frequency)
            cur_frequency += change


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
