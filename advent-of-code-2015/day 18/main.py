"""Advent of Code 2015 Day 18."""
from functools import lru_cache

ON = '#'
OFF = '.'
CORNERS = ((0, 0), (0, -1), (-1, 0), (-1, -1))


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    grid = parse_grid(lines)
    grid_after = make_n_steps(grid, 100, make_step)
    lights_on = count_lights_on(grid_after)
    print(f'Lights on after 100 steps: {lights_on}')
    grid_with_stuck = stuck_corners(make_n_steps(grid, 100, make_stuck_step))
    lights_on_stuck = count_lights_on(grid_with_stuck)
    print(f'Lights on after 100 steps with corners stuck: {lights_on_stuck}')


def make_step(old_grid):
    """Make single step on old_grid."""
    grid = copy_grid(old_grid)
    grid_size = get_grid_size(old_grid)
    for row_no, row in enumerate(old_grid):
        for col_no, light in enumerate(row):
            neighbours = get_neighbour_coordinates(row_no, col_no, grid_size)
            neighbours_on = get_number_on(get_lights(neighbours, old_grid))
            if light == ON and neighbours_on not in (2, 3):
                grid[row_no][col_no] = OFF
            elif light == OFF and neighbours_on == 3:
                grid[row_no][col_no] = ON
    return grid


def get_number_on(lights):
    """Count number of lights on in the list."""
    return lights.count(ON)


def get_lights(lights, grid):
    """Get lights states from grid for lights list."""
    return [grid[row][col] for row, col in lights]


def make_stuck_step(grid):
    """Make step on grid after lighting corners."""
    return make_step(stuck_corners(grid))


def stuck_corners(grid):
    """Keep stuck corners on."""
    for row, col in CORNERS:
        grid[row][col] = ON
    return grid


def make_n_steps(grid, n, stepper):
    """Make n number of steps on grid with stepper function."""
    for _ in range(n):
        grid = stepper(grid)
    return grid


@lru_cache()
def get_neighbour_coordinates(row, col, grid_size):
    """Get coordinates of neighbour lights to row and col for grid_size."""
    max_row, max_col = [num - 1 for num in grid_size]
    neighbours = []
    for row_number in (row - 1, row, row + 1):
        if not is_in_grid(row_number, max_row):
            continue
        for column_number in (col - 1, col, col + 1):
            if ((row_number, column_number) == (row, col)
                    or not is_in_grid(column_number, max_col)):
                continue
            neighbours.append((row_number, column_number))
    return neighbours


def is_in_grid(index, maximum):
    """Check if index is within grid range."""
    return 0 <= index <= maximum


def get_grid_size(grid):
    """Get size of grid and grid's row."""
    return len(grid), len(grid[0])


def copy_grid(grid):
    """Copy grid."""
    return [row[:] for row in grid]


def parse_grid(lines):
    """Parse grid from lines to list of lists."""
    return [list(line) for line in lines]


def count_lights_on(grid):
    """Count number of lights on in grid."""
    return sum(row.count(ON) for row in grid)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
