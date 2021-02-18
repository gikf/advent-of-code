"""Advent of Code 2017 Day 3."""


puzzle = 289326
NEIGHBOURS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def main(puzzle=puzzle):
    print(f'Steps from {puzzle} to 1: {find_distance_from_1_to(puzzle)}')
    print(f'First value higher than {puzzle}: '
          f'{find_first_higher_than(puzzle)}')


def find_first_higher_than(number):
    """Find in square first value higher than number."""
    grid = [[1]]
    last_val = 1
    while True:
        grid = expand_grid(grid)
        row = len(grid) - 1
        col = len(grid) - 1

        for row_change, col_change in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            for _ in range(len(grid) - 1):
                row += row_change
                col += col_change
                last_val = sum(get_neighbour_values(grid, row, col))
                grid[row][col] = last_val
                if last_val > number:
                    return last_val


def get_neighbour_values(grid, row, column):
    """Get neighbour values of row and column in grid."""
    neighbours = []
    for row_change, col_change in NEIGHBOURS:
        next_row = row + row_change
        next_col = column + col_change
        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid):
            neighbours.append(grid[row + row_change][column + col_change])
    return neighbours


def expand_grid(grid):
    """Expand grid by one in every direction."""
    new_length = len(grid) + 2
    row = [0 for _ in range(new_length)]
    new_grid = [[0] + row + [0] for row in grid]
    return [row[:]] + new_grid + [row[:]]


def find_distance_from_1_to(number):
    """Find Manhattan Distance between number and 1 in square."""
    last_corner = 1
    steps = 1
    side = 0
    while last_corner < number:
        if side == 0:
            steps += 2
        last_corner += steps - 1
        side += 1
        if side == 4:
            side = 0
    to_middle = (steps - 1) // 2
    middle = last_corner - to_middle
    return to_middle + abs(number - middle)


if __name__ == '__main__':
    main()
