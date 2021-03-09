"""Advent of Code 2017 Day 22."""

INFECTED = '#'
CLEAN = '.'
WEAKENED = 'W'
FLAGGED = 'F'
DIRECTION_TO_MOVE = {
    90: (-1, 0),
    0: (0, 1),
    180: (0, -1),
    270: (1, 0),
}
SIDES = {
    'right': -90,
    'left': 90,
    'reverse': 180,
}


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    bursts = (
        (10_000, actions, 'normal'),
        (10_000_000, evolved_actions, 'evolved'),
    )
    for number, node_actions, description in bursts:
        grid = parse_grid(lines)
        start = (len(grid) // 2, len(grid[0]) // 2)
        caused_infections = burst_n_times(grid, start, number, node_actions())
        print(f'Infections caused during {number} number of {description} '
              f'bursts: {caused_infections}')


def burst_n_times(grid, start, n, node_actions):
    """Burst n times from start on grid, using node_actions."""
    cur_node = start
    direction = 90
    caused_infections = 0
    for _ in range(n):
        cur_row, cur_col = cur_node
        node_type = grid[cur_row][cur_col]
        action = node_actions[node_type]
        count, node_type, direction = action(direction)
        caused_infections += count
        grid[cur_row][cur_col] = node_type
        cur_node, grid = move_forward(grid, cur_row, cur_col, direction)
    return caused_infections


def actions():
    """Return mapping of normal virus from node type to node action."""
    return {
        CLEAN: clean,
        INFECTED: infected,
    }


def evolved_actions():
    """Return mapping of evolved virus from node type to node action."""
    return {
        CLEAN: clean_evolved,
        INFECTED: infected_evolved,
        WEAKENED: weakened,
        FLAGGED: flagged,
    }


def weakened(direction):
    """Weakened node action."""
    return 1, INFECTED, direction


def clean(direction):
    """Clean node action."""
    return 1, INFECTED, turn(direction, 'left')


def clean_evolved(direction):
    """Evolved clean node action."""
    return 0, WEAKENED, turn(direction, 'left')


def infected(direction):
    """Infected node action."""
    return 0, CLEAN, turn(direction, 'right')


def infected_evolved(direction):
    """Evolved infected node action."""
    return 0, FLAGGED, turn(direction, 'right')


def flagged(direction):
    """Flagged node action."""
    return 0, CLEAN, turn(direction, 'reverse')


def move_forward(grid, cur_row, cur_col, direction):
    """Move current row, col forward in direction.

    If move goes outside of current grid, then add additional
    row or column on that side."""
    row_change, col_change = DIRECTION_TO_MOVE[direction]
    next_row = cur_row + row_change
    next_col = cur_col + col_change
    if next_row < 0:
        grid = [[CLEAN for _ in range(len(grid[0]))]] + grid
        next_row = 0
    elif next_row == len(grid):
        grid = grid + [[CLEAN for _ in range(len(grid[0]))]]
    elif next_col < 0:
        next_col = 0
        grid = [[CLEAN] + row[:] for row in grid]
    elif next_col == len(grid[0]):
        grid = [row[:] + [CLEAN] for row in grid]
    return (next_row, next_col), grid


def turn(old_direction, side):
    """Turn old_direction depending on the side."""
    return (old_direction + SIDES[side]) % 360


def parse_grid(lines):
    """Parse lines to grid."""
    return [[*row] for row in lines]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
