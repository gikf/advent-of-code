# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:07:42 2020
"""
from functools import lru_cache


ACTIVE = '#'
INACTIVE = '.'


def main():
    initial_grid = load_initial_grid(
        [line.strip() for line in get_file_contents()])
    final_grid = cycle_grid_n_times(initial_grid, 6, cycle_grid)
    print(count_active_in_grid(final_grid))
    print('Four dimension:')
    initial_grid4 = load_initial_grid4(
        [line.strip() for line in get_file_contents()])
    final_grid4 = cycle_grid_n_times(initial_grid4, 6, cycle_grid4)
    print(count_active_in_grid4(final_grid4))


def cycle_grid_n_times(grid, n, cycler):
    """Cycle grid n times using cycler."""
    final_grid = grid
    for _ in range(n):
        final_grid = cycler(final_grid)
    return final_grid


def cycle_grid(grid):
    grid = expand_grid(grid)
    x, y, z = get_grid_size(grid)
    new_grid = create_empty_grid(x, y, z)
    for dim_no, dimension in enumerate(grid):
        for row_no, row in enumerate(dimension):
            for col_no, column in enumerate(row):
                point = (col_no, row_no, dim_no)
                active_neighbours = count_active_for(point, grid)
                new_grid[dim_no][row_no][col_no] = get_new_value(
                    column, active_neighbours)
    return new_grid


def cycle_grid4(grid):
    grid = expand_grid(grid)
    x, y, z, w = get_grid_size(grid)
    new_grid = create_empty_grid4(x, y, z, w)
    for w_no, one_w in enumerate(grid):
        for dim_no, dimension in enumerate(one_w):
            for row_no, row in enumerate(dimension):
                for col_no, column in enumerate(row):
                    point = (col_no, row_no, dim_no, w_no)
                    active_neighbours = count_active_for(point, grid)
                    new_grid[w_no][dim_no][row_no][col_no] = get_new_value(
                        column, active_neighbours)
    return new_grid


def get_new_value(value, active_neighbours):
    """Get new value based on number of active_neighbours."""
    if value == ACTIVE and active_neighbours not in (2, 3):
        return INACTIVE
    elif value == INACTIVE and active_neighbours == 3:
        return ACTIVE
    return value


def load_initial_grid4(state_slice):
    grid = []
    grid.append([[
        [column for column in row]
        for row in state_slice
    ]])
    return grid


def expand_grid(grid):
    """Expand grid, by two and readd old values to new grid."""
    old_size = get_grid_size(grid)
    new_size = [size + 2 for size in old_size]
    if len(old_size) == 4:
        new_grid = create_empty_grid4(*new_size)
        for w_no, w in enumerate(grid):
            for dim_no, dimension in enumerate(w):
                for row_no, row in enumerate(dimension):
                    new_grid[w_no + 1][dim_no + 1][row_no + 1][1:-1] = row[:]
    elif len(old_size) == 3:
        new_grid = create_empty_grid(*new_size)
        for dim_no, dimension in enumerate(grid):
            for row_no, row in enumerate(dimension):
                new_grid[dim_no + 1][row_no + 1][1:-1] = row[:]
    return new_grid


def get_grid_size(grid):
    """Get sizes of grid."""
    sizes = []
    sub_grid = grid
    while isinstance(sub_grid, list):
        sizes.append(len(sub_grid))
        sub_grid = sub_grid[0]
    return sizes[::-1]


def count_active_for(point, grid):
    """Count active neighbours in grid for point."""
    if len(point) == 4:
        neighbours = get_neighbours4(*point)
    elif len(point) == 3:
        neighbours = get_neighbours(*point)
    count = 0
    for neighbour in neighbours:
        if is_active(get_point_state(neighbour, grid)):
            count += 1
    return count


def get_point_state(point, grid):
    """Get state of the point from grid."""
    try:
        element = grid
        for coord in point[::-1]:
            element = element[coord]
        return element
    except IndexError:
        return INACTIVE


def count_active_in_grid4(grid):
    return sum(
        row.count(ACTIVE)
        for one_w in grid
        for dimension in one_w
        for row in dimension
    )


def create_empty_grid4(columns, rows, dimensions, ws):
    return [
        [
            [
                [INACTIVE for _ in range(columns)]
                for _ in range(rows)
            ]
            for _ in range(dimensions)
        ]
        for _ in range(ws)
    ]


@lru_cache()
def get_neighbours4(x, y, z, w):
    neighbours = []
    for nx in (x - 1, x, x + 1):
        for ny in (y - 1, y, y + 1):
            for nz in (z - 1, z, z + 1):
                for nw in (w - 1, w, w + 1):
                    if (any(num < 0 for num in (nx, ny, nz, nw))
                            or (x, y, z, w) == (nx, ny, nz, nw)):
                        continue
                    neighbours.append((nx, ny, nz, nw))
    return neighbours


def load_initial_grid(state_slice):
    grid = []
    grid.append([
        [column for column in row]
        for row in state_slice
    ])
    return grid


def create_empty_grid(columns, rows, dimensions):
    return [
        [
            [INACTIVE for _ in range(columns)]
            for _ in range(rows)
        ]
        for _ in range(dimensions)
    ]


def count_active_in_grid(grid):
    return sum(
        row.count(ACTIVE)
        for dimension in grid
        for row in dimension
    )


def is_active(state):
    """Check if state is ACTIVE."""
    return state == ACTIVE


@lru_cache()
def get_neighbours(x, y, z):
    neighbours = []
    for nx in (x - 1, x, x + 1):
        for ny in (y - 1, y, y + 1):
            for nz in (z - 1, z, z + 1):
                if (any(num < 0 for num in (nx, ny, nz))
                        or (x, y, z) == (nx, ny, nz)):
                    continue
                neighbours.append((nx, ny, nz))
    return neighbours


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
