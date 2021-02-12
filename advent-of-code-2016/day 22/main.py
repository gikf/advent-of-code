"""Advent of Code 2016 Day 22."""
from collections import deque
import re

EMPTY = 'O'
FULL = '#'
NORMAL = '.'
GOAL = 'G'
MOVES = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
)


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)[2:]]
    disks = parse_disks(lines)
    pairs_number = find_number_pairs(disks)
    print(f'Number of pairs possible to move: {pairs_number}')
    grid = create_grid(disks)
    print('Grid for part 2:')
    for row in grid:
        print(' '.join(row))
    empty_cell = [disk
                  for disk in disks
                  if disk['use_percent'] == 0][0]['position'][::-1]
    steps_from_empty_to_top_right = find_min_steps(empty_cell, (0, 29), grid)
    steps_from_top_right_top_left = 28 * 5
    total = steps_from_empty_to_top_right + steps_from_top_right_top_left
    print('Steps from empty cell to top-right: '
          f'{steps_from_empty_to_top_right}')
    print('Steps from top-right to top-left: '
          f'{steps_from_top_right_top_left}')
    print(f'In total: {total}')


def find_min_steps(source, target, grid):
    """Find minimum number of steps from source to target on grid."""
    grid_steps = get_grid(32, 30)
    source_row, source_col = source
    grid_steps[source_row][source_col] = 0
    visited = set()
    queue = deque([source])
    while queue:
        cur_position = queue.popleft()
        cur_row, cur_col = cur_position
        if cur_position == target:
            return grid_steps[cur_row][cur_col]
        elif cur_position in visited:
            continue
        visited.add(cur_position)
        next_steps = grid_steps[cur_row][cur_col] + 1
        for change_row, change_col in MOVES:
            next_row = cur_row + change_row
            next_col = cur_col + change_col
            if not is_in_limit(next_row, 32) or not is_in_limit(next_col, 30):
                continue
            next_cell = grid[next_row][next_col]
            if not can_be_visited(next_cell, grid_steps[next_row][next_col]):
                continue
            grid_steps[next_row][next_col] = next_steps
            queue.append((next_row, next_col))
    return -1


def can_be_visited(next_cell, steps):
    """Check if next_cell and steps make cell visit-able."""
    return next_cell in (GOAL, NORMAL) and steps == -1


def is_in_limit(value, limit):
    """Check if value is within limit."""
    return 0 <= value < limit


def create_grid(disks):
    """Create grid fitting all disks and mark them according to use percent."""
    grid = get_grid(32, 30)
    for disk in disks:
        column, row = disk['position']
        grid[row][column] = get_mark(disk['used'])
    grid[0][29] = GOAL
    return grid


def get_grid(rows, columns):
    """Get grid with number rows and columns."""
    return [[-1 for _ in range(columns)]
            for _ in range(rows)]


def get_mark(value):
    """Get mark for grid corresponding to the value."""
    if value == 0:
        return EMPTY
    elif value >= 95:
        return FULL
    else:
        return NORMAL


def find_number_pairs(disks):
    """Find number of pairs in disks that can be swapped."""
    count = 0
    sorted_available = sorted(
        [disk['available'] for disk in disks], reverse=True)
    maximum = sorted_available[0]
    for disk in disks:
        if disk['used'] == 0 or disk['used'] > maximum:
            continue
        disks_num, space_needed = get_viable_disks(
            disk['used'], maximum, sorted_available)
        if disk['available'] >= space_needed:
            disks_num -= 1
        count += disks_num + 1
    return count


def get_viable_disks(space_needed, maximum, sorted_available):
    """Get number of disks that can fit at least space_needed."""
    disks_num = -1
    while space_needed <= maximum and disks_num == -1:
        try:
            disks_num = sorted_available.index(space_needed)
        except ValueError:
            space_needed += 1
    return disks_num, space_needed


def parse_disks(lines):
    """Parse lines to disks."""
    return [parse_disk(line) for line in lines]


def parse_disk(line):
    """Parse line to dictionary representing disk."""
    position, *rest = line.split()
    position = tuple([int(num) for num in re.findall(r'(\d+)', position)])
    size, used, available, use_percent = [int(value[:-1]) for value in rest]
    return {
        'position': position,
        'size': size,
        'used': used,
        'available': available,
        'use_percent': use_percent,
    }


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
