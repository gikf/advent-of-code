"""Advent of Code 2017 Day 11."""


directions = {
    'n': (0, 1, -1),
    's': (0, -1, 1),
    'ne': (1, 0, -1),
    'sw': (-1, 0, 1),
    'nw': (-1, 1, 0),
    'se': (1, -1, 0),
}


def main(file_input='input.txt'):
    path = get_file_contents(file_input)[0].strip().split(',')
    steps_away, most_steps_away = find_steps_away(path)
    print(f'Steps away: {steps_away}')
    print(f'Most steps away: {most_steps_away}')


def find_steps_away(path):
    """Find number steps away after following path, and furthest distance."""
    position = [0, 0, 0]
    most_steps_away = 0
    for step in path:
        position = [coordinate + change
                    for coordinate, change in zip(position, directions[step])]
        most_steps_away = max(most_steps_away, calculate_steps(position))
    return calculate_steps(position), most_steps_away


def calculate_steps(position):
    """Calculate steps to the position."""
    return max(abs(num) for num in position)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
