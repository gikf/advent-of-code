"""Advent of Code 2018 Day 11."""


puzzle = 7400


def main(puzzle=puzzle):
    grid = get_grid(300, 300)
    filled_grid = fill_grid(grid, serial_number=puzzle)
    coordinates, largest_sub_grid_value = find_largest_sub_grid(filled_grid)
    print('Top-left coordinate of 3x3 square with the largest total power:',
          ','.join(str(num) for num in coordinates))
    coordinates, size, largest_sub_grid_value = (
        find_largest_any_size_sub_grid(filled_grid))
    print('X,Y,size of square with the largest total power:',
          ','.join(str(num) for num in [*coordinates, size]))


def find_largest_any_size_sub_grid(grid):
    """Find largest sub grid of any size on grid."""
    size_values = []
    for cur_size in range(2, len(grid) + 1):
        coordinates, cur_largest_value = find_largest_sub_grid(
            grid, cur_size
        )
        size_values.append((coordinates, cur_size, cur_largest_value))
        if cur_largest_value < 0:
            break
    return max(size_values, key=lambda item: item[2])


def find_largest_sub_grid(grid, size=3):
    """Find largest sub grid of size on grid."""
    cur_grid_value = None
    grid_values = []
    for row_no, row in enumerate(grid[:-size]):
        for col_no, _ in enumerate(row[:-size]):
            if cur_grid_value is None:
                cur_grid_value = get_grid_value(grid, row_no, col_no, size)
                prev_row_val = cur_grid_value
            elif col_no == 0:
                cur_grid_value = move_row_in_grid_value(
                    grid, prev_row_val, row_no, col_no, size)
                prev_row_val = cur_grid_value
            else:
                cur_grid_value = move_column_in_grid_value(
                    grid, cur_grid_value, row_no, col_no, size)
            grid_values.append(((col_no + 1, row_no + 1), cur_grid_value))
    return max(grid_values, key=lambda item: item[1])


def move_row_in_grid_value(grid, value, row, col, size):
    """Subtract value of row before sub grid and add last row of it."""
    prev_row = sum(grid[row - 1][col:col + size])
    last_row = sum(grid[row - 1 + size][col:col + size])
    return value - prev_row + last_row


def move_column_in_grid_value(grid, value, row, col, size):
    """Subtract value of column before sub grid and add last column of it."""
    prev_col = sum_col(grid, col - 1, row, size)
    last_col = sum_col(grid, col - 1 + size, row, size)
    return value - prev_col + last_col


def sum_col(grid, col, row, size):
    """Sum values in column for rows - row:row + size."""
    return sum(
        cur_row[col]
        for cur_row in grid[row:row + size]
    )


def get_grid_value(grid, row, col, size):
    """Get value of grid, starting from (row, col) and with size."""
    return sum(
        sum(cur_row[col:col + size])
        for cur_row in grid[row: row + size]
    )


def fill_grid(grid, serial_number):
    """Fill grid with power levels based on serial_number."""
    for row_no, row in enumerate(grid):
        for col_no, _ in enumerate(row):
            grid[row_no][col_no] = get_power_level(
                row_no + 1, col_no + 1, serial_number)
    return grid


def get_power_level(row, col, serial_number):
    """Calculate power level for coordinate (col, row) and serial_number."""
    rack_id = col + 10
    starting_power_level = rack_id * row
    increased_power_level = starting_power_level + serial_number
    power_level = increased_power_level * rack_id
    hundreth_digit = (power_level // 100) % 10
    final_power_level = hundreth_digit - 5
    return final_power_level


def get_grid(rows, columns):
    """Get grid with number of rows and columns."""
    return [[0 for _ in range(columns)]
            for _ in range(rows)]


if __name__ == '__main__':
    main()
