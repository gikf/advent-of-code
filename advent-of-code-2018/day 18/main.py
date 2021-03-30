"""Advent of Code 2018 Day 18."""


OPEN = '.'
TREES = '|'
LUMBERYARD = '#'
ADJACENT = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def main(file_input='input.txt'):
    grid = [[*line.strip()] for line in get_file_contents(file_input)]
    runs = (
        ('10', 10),
        ('1 billion', 1_000_000_000),
    )
    for description, minutes in runs:
        ending_grid = pass_time(grid, minutes)
        lumber_value = count_total_lumber_value(ending_grid)
        print(f'Lumber value after {description} minutes: {lumber_value}')


def pass_time(grid, minutes):
    """Pass number of minutes on grid."""
    cur_grid = copy_grid(grid)
    grid_set = get_grid_for_set(cur_grid)
    grid_set_to_minute = {grid_set: 0}
    minute_to_grid_set = {0: grid_set}
    for minute in range(1, minutes + 1):
        cur_grid = pass_minute(cur_grid)
        cur_grid_set = get_grid_for_set(cur_grid)
        if cur_grid_set in grid_set_to_minute:
            prev_minute = grid_set_to_minute[cur_grid_set]
            ending_minute = get_ending_minute_after_loop(
                minutes, minute, prev_minute)
            return minute_to_grid_set[ending_minute]
        grid_set_to_minute[cur_grid_set] = minute
        minute_to_grid_set[minute] = cur_grid_set
    return cur_grid


def get_ending_minute_after_loop(minutes, minute, prev_minute):
    """Get number of minutes after loop end to reach wanted minutes."""
    loop_length = minute - prev_minute
    minutes_left = minutes - minute
    full_loops = minutes_left // loop_length
    minutes_in_loop = loop_length * full_loops
    return prev_minute + minutes_left - minutes_in_loop


def get_grid_for_set(grid):
    """Return grid joined into hashable representation."""
    return ''.join(''.join(row) for row in grid)


def pass_minute(initial_grid):
    """Pass one minute on initial_grid. Return new copy of grid."""
    grid = copy_grid(initial_grid)
    for row_no, row in enumerate(initial_grid):
        for col_no, cur_acre in enumerate(row):
            new_acre = get_new_acre(initial_grid, cur_acre, row_no, col_no)
            if new_acre != cur_acre:
                grid[row_no][col_no] = new_acre
    return grid


def get_new_acre(grid, cur_acre, row, col):
    """Get new acre for (row, col) on grid."""
    adjacent_acres = get_acres(
        grid, get_adjacent(row, col))
    adjacent_trees = count_in_acres(adjacent_acres, TREES)
    adjacent_lumber = count_in_acres(adjacent_acres, LUMBERYARD)
    if cur_acre == OPEN and adjacent_trees >= 3:
        return TREES
    elif cur_acre == TREES and adjacent_lumber >= 3:
        return LUMBERYARD
    elif cur_acre == LUMBERYARD and (
            adjacent_trees == 0 or adjacent_lumber == 0):
        return OPEN
    return cur_acre


def count_in_acres(acres, wanted):
    """Count how many wanted acres are among acres."""
    return len([acre for acre in acres if acre == wanted])


def count_total_lumber_value(grid):
    """Count total lumber value. Multiply numbers of TREES and LUMBERYARD."""
    wooded = sum(row.count(TREES) for row in grid)
    lumbery = sum(row.count(LUMBERYARD) for row in grid)
    return wooded * lumbery


def get_acres(grid, coordinates):
    """Get acres from coordinates on grid."""
    acres = []
    for row, column in coordinates:
        if 0 <= row < len(grid) and 0 <= column < len(grid[0]):
            acres.append(grid[row][column])
    return acres


def get_adjacent(row, col):
    """Get adjacent acres to (row, col)."""
    adjacent = []
    for change_row, change_col in ADJACENT:
        next_row = row + change_row
        next_col = col + change_col
        adjacent.append((next_row, next_col))
    return adjacent


def copy_grid(grid):
    """Return copy of grid."""
    return [row[:] for row in grid]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
