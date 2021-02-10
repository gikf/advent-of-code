"""Advent of Code 2016 Day 20."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    ranges = parse_ranges(lines)
    sorted_ranges = sorted(ranges, key=lambda item: item[0])
    allowed = sorted(find_allowed(sorted_ranges))
    print(f'First allowed IP: {allowed[0]}')
    print(f'Allowed IPs in total: {len(allowed)}')


def find_allowed(ranges, limit=4294967295):
    """Find allowed IPs for ranges and with limit."""
    last_number = 0
    allowed = []
    for minimum, maximum in ranges:
        if last_number + 1 >= minimum:
            last_number = max(last_number, maximum)
        else:
            while last_number + 1 < minimum:
                allowed.append(last_number + 1)
                last_number += 1
            last_number = maximum
    while last_number < limit:
        allowed.append(last_number + 1)
        last_number += 1
    return allowed


def parse_ranges(lines):
    """Parse lines to ranges."""
    return [parse_range(line) for line in lines]


def parse_range(line):
    """Parse line to list with two numbers."""
    return [int(num) for num in line.split('-')]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
