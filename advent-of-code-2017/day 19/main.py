"""Advent of Code 2017 Day 19."""

LINES = '|-+'
EMPTY = ' '
DIRECTIONS = {
    'down': (1, 0),
    'up': (-1, 0),
    'left': (0, -1),
    'right': (0, 1),
}
DIRECTION_TO_PLANE = {
    'down': 0,
    'up': 0,
    'left': 1,
    'right': 1,
}


def main(file_input='input.txt'):
    lines = [line.strip('\n') for line in get_file_contents(file_input)]
    start = (0, lines[0].index('|'))
    letters, steps = follow_diagram(lines, start)
    print(letters, steps)


def follow_diagram(lines, start):
    """Follow diagram in lines from start."""
    cur_row, cur_col = start
    direction = 'down'
    letters = []
    steps = 0
    while lines[cur_row][cur_col] != EMPTY:
        steps += 1
        row_change, col_change = DIRECTIONS[direction]
        cur_row += row_change
        cur_col += col_change
        cur_cell = lines[cur_row][cur_col]
        if cur_cell.isalpha():
            letters.append(cur_cell)
        if cur_cell != '+':
            continue
        direction = get_next_direction(lines, direction, cur_row, cur_col)
    return (''.join(letters), steps)


def get_next_direction(lines, cur_direction, cur_row, cur_col):
    """Get next direction from the (cur_row, cur col)."""
    for direction, (row_change, col_change) in DIRECTIONS.items():
        next_row = cur_row + row_change
        next_col = cur_col + col_change
        next_cell = lines[next_row][next_col]
        if (next_cell == EMPTY or next_cell == '+'
                or are_planes_the_same(direction, cur_direction)):
            continue
        return direction


def are_planes_the_same(direction, next):
    """Check if direction and next are on the same plane."""
    return DIRECTION_TO_PLANE[direction] == DIRECTION_TO_PLANE[next]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
