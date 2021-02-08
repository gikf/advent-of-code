"""Advent of Code 2016 Day 18."""

SAFE = '.'
TRAP = '^'


def main(file_input='input.txt'):
    line = get_file_contents(file_input)[0].strip()
    for number_of_rows in (40, 400_000):
        safe_tiles = get_safe_tiles_count(line, number_of_rows)
        print(f'Safe tiles in {number_of_rows} rows: {safe_tiles}')


def get_safe_tiles_count(line, number_of_rows):
    """Get number of safe tiles in length rows, including starting line."""
    last_line = line
    safe_tiles = count_safe_tiles(line)
    for row_no in range(number_of_rows - 1):
        next_row = []
        for col_no, col in enumerate(last_line):
            if is_next_tile_trap(get_tiles(last_line, col_no)):
                next_row.append(TRAP)
            else:
                next_row.append(SAFE)
        last_line = next_row
        safe_tiles += count_safe_tiles(next_row)
    return safe_tiles


def get_tiles(row, column_no):
    """Get tiles from row besides and including column_no."""
    tile_numbers = (column_no - 1, column_no, column_no + 1)
    tiles = []
    for tile_number in tile_numbers:
        if tile_number < 0 or tile_number == len(row):
            tiles.append(SAFE)
        else:
            tiles.append(row[tile_number])
    return tiles


def is_next_tile_trap(prev_tiles):
    """Check if next tile is trap."""
    left, center, right = prev_tiles
    return left != right


def count_safe_tiles(line):
    """Count number of SAFE tiles in line."""
    return line.count(SAFE)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
