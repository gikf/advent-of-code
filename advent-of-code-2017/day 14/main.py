"""Advent of Code 2017 Day 14."""

puzzle = 'stpzcrnm'
example = 'flqrgnkx'
USED = '#'
FREE = '.'
ADJACENT = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def main(puzzle=puzzle):
    grid = get_grid_from(puzzle)
    print(f'Used squares: {count_used(grid)}')
    regions = get_regions(grid)
    print(f'Number of regions: {len(regions)}')


def get_regions(grid):
    """Get all regions on grid."""
    regions = {}
    visited = set()
    cur_region = 0
    for row_no, row in enumerate(grid):
        for col_no, col in enumerate(row):
            if (row_no, col_no) in visited or col != USED:
                continue
            region = visit_region(grid, row_no, col_no)
            regions[cur_region] = region
            cur_region += 1
            visited = visited | region
    return regions


def visit_region(grid, row_no, col_no):
    """Visit on grid region starting at row_no, col_no."""
    region = set()
    visited = set()
    stack = [(row_no, col_no)]
    while stack:
        cur_square = stack.pop()
        if cur_square in visited:
            continue
        visited.add(cur_square)
        cur_row, cur_col = cur_square
        if grid[cur_row][cur_col] != USED:
            continue
        region.add(cur_square)
        stack.extend(get_adjacent_squares(grid, cur_row, cur_col))
    return region


def get_adjacent_squares(grid, cur_row, cur_col):
    """Get adjacent squares for square at cur_row, cur_col."""
    squares = []
    for row_change, col_change in ADJACENT:
        next_row = cur_row + row_change
        next_col = cur_col + col_change
        if in_limit(next_row, len(grid)) and in_limit(next_col, len(grid[0])):
            squares.append((next_row, next_col))
    return squares


def in_limit(value, limit):
    """Check if value is in limit."""
    return 0 <= value < limit


def get_grid_from(key):
    """Get grid filled from key."""
    grid = []
    for number in range(128):
        list_ = [num for num in range(256)]
        lengths = (
            [ord(char) for char in f'{key}-{number}'] + [17, 31, 73, 47, 23])
        sparse_hash = rounds(list_[:], lengths, 64)
        dense_hash = get_dense_hash(sparse_hash)
        cur_row = []
        for digit in dense_hash:
            binary = bin(int(digit, 16))
            cur_row.append(''.join(USED if digit == '1' else FREE
                                   for digit in binary[2:].zfill(4)))
        grid.append(''.join(cur_row))
    return grid


def get_dense_hash(sparse_hash):
    """Get dense hash from sparse hash."""
    dense_hash = []
    cur_number = None
    counter = 0
    for number in sparse_hash:
        if counter == 15:
            cur_number = cur_number ^ number
            hexed = hex(cur_number)[2:]
            dense_hash.append(f'{hexed:0>2}')
            cur_number = None
            counter = 0
            continue

        if cur_number is None:
            cur_number = number
        else:
            cur_number = cur_number ^ number
        counter += 1
    return ''.join(dense_hash)


def rounds(list_, lengths, rounds):
    """Perform knotting number of rounds on list_ using lengths values."""
    position = 0
    skip = 0
    for _ in range(rounds):
        _, position, skip = knot_list(list_, lengths, position, skip)
    return list_


def knot_list(list_, lengths, position=0, skip=0):
    """Knot list_ using lengths values, starting with position and skip."""
    wrap_at = len(list_)
    for length in lengths:
        start = position
        end = position + length
        if end > wrap_at:
            reverse_with_wrap(list_, start, end, wrap_at)
        else:
            list_[start:end] = list_[start:end][::-1]
        position = (position + length + skip) % wrap_at
        skip += 1
    return list_, position, skip


def reverse_with_wrap(list_, start, end, wrap_at):
    """Reverse list_ from start to end wrapping back to beginning of list."""
    length_to_end = wrap_at - start
    length_from_start = end % wrap_at
    reverse = (list_[start:] + list_[:length_from_start])[::-1]
    list_[start:] = reverse[0:length_to_end]
    list_[:length_from_start] = reverse[length_to_end:]


def count_used(grid):
    return sum(row.count(USED) for row in grid)


if __name__ == '__main__':
    main()
