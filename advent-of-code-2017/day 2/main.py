"""Advent of Code 2017 Day 2."""


def main(file_input='input.txt'):
    spreadsheet = [[int(num) for num in line.strip().split()]
                   for line in get_file_contents(file_input)]
    checksum_max_min = sum(max(row) - min(row) for row in spreadsheet)
    print('Checksum based on difference between largest and lowest number in '
          f'row: {checksum_max_min}')
    divisable = [get_divisable(row) for row in spreadsheet]
    checksum_divisible = sum(num_1 / num_2 for num_1, num_2 in divisable)
    print('Checksum based on evenly divisible numbers in row '
          f'{checksum_divisible:.0f}')


def get_divisable(row):
    """Get numbers from row where one divides another without rest."""
    for index, num in enumerate(row[:-1]):
        for other_num in row[index + 1:]:
            if num % other_num == 0 or other_num % num == 0:
                return sorted([num, other_num], reverse=True)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
