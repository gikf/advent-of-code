"""Advent of Code 2019 Day 24."""
from copy import deepcopy
from functools import lru_cache


BUG = '#'
EMPTY = '.'
MOVES = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)
ADJACENT_LEVELS = {
    (1, 2): [1, [(0, value) for value in range(5)]],
    (2, 1): [1, [(value, 0) for value in range(5)]],
    (2, 3): [1, [(value, 4) for value in range(5)]],
    (3, 2): [1, [(4, value) for value in range(5)]],
    (0, 0): [-1, [(2, 1), (1, 2)]],
    (4, 4): [-1, [(2, 3), (3, 2)]],
    (0, 4): [-1, [(1, 2), (2, 3)]],
    (4, 0): [-1, [(2, 1), (3, 2)]],
}
for value in range(1, 4):
    ADJACENT_LEVELS[(value, 0)] = [-1, [(2, 1)]]
    ADJACENT_LEVELS[(0, value)] = [-1, [(1, 2)]]
    ADJACENT_LEVELS[(value, 4)] = [-1, [(2, 3)]]
    ADJACENT_LEVELS[(4, value)] = [-1, [(3, 2)]]


def main(file_input='input.txt'):
    eris = [[*line.strip()] for line in get_file_contents(file_input)]
    repeating_layout = find_repeating_layout(eris)
    biodiversity = count_biodiversity(repeating_layout)
    print(f'Biodiversity of first repeating layout: {biodiversity}')
    recursive_eris = {0: [[*row] for row in eris]}
    eris_after_200_minutes = pass_minutes(recursive_eris, 200)
    bugs_on_eris = count_bugs(eris_after_200_minutes)
    print(f'Bugs on eris after 200 minutes: {bugs_on_eris}')


def pass_minutes(eris, minutes):
    """Pass number of minutes on recursive eris."""
    for _ in range(minutes):
        recursive_eris = deepcopy(eris)
        expand_eris(recursive_eris)
        eris = pass_minute_recursive_levels(eris, recursive_eris)
    return eris


def pass_minute_recursive_levels(initial_eris, recursive_eris):
    """Pass minute on recursive levels based on initial_eris."""
    for level, eris in recursive_eris.items():
        for row_no, row in enumerate(eris):
            for col_no, tile in enumerate(row):
                if row_no == 2 and col_no == 2:
                    continue
                adjacent_coordinates = get_recursive_adjacent(row_no, col_no)
                adjacent_tiles = get_adjacent_tiles(
                    initial_eris, level, adjacent_coordinates)
                adjaceng_bug_count = adjacent_tiles.count(BUG)
                new_tile = get_new_tile(tile, adjaceng_bug_count)
                if new_tile != tile:
                    recursive_eris[level][row_no][col_no] = new_tile
    return recursive_eris


def get_new_tile(cur_tile, adjacent_bug_count):
    """Get new tile, based on cur_tile and adjacent_bug_count."""
    if cur_tile == BUG and adjacent_bug_count != 1:
        return EMPTY
    elif cur_tile == EMPTY and adjacent_bug_count in (1, 2):
        return BUG
    return cur_tile


def get_adjacent_tiles(eris, level, coordinates):
    """Get adjacent tiles from coordinates at level on eris."""
    adjacent = []
    for level_change, (row, col) in coordinates:
        if row == 2 and col == 2:
            continue
        try:
            adjacent.append(
                eris[level + level_change][row][col])
        except KeyError:
            pass
    return adjacent


def get_recursive_adjacent(row, col):
    """Get adjacent tiles for the recursive levels."""
    coordinates = [
        (0, pair)
        for pair in get_adjacent_coordinates(row, col)]
    level_change, level_adjacent = ADJACENT_LEVELS.get(
        (row, col), (None, []))
    for pair in level_adjacent:
        coordinates.append((level_change, pair))
    return coordinates


def get_boundary_levels(eris):
    """Get boundary levels for eris."""
    return [func(eris.keys()) for func in (min, max)]


def expand_eris(recursive_eris):
    """Expand recursive eris when boundary levels have at least one BUG."""
    minimum, maximum = get_boundary_levels(recursive_eris)
    for level, change in ((minimum, -1), (maximum, 1)):
        if any(BUG in row for row in recursive_eris[level]):
            recursive_eris[level + change] = get_new_level()


def get_new_level(size=5):
    """Get new size x size level."""
    return [[EMPTY for _ in range(size)] for _ in range(size)]


def find_repeating_layout(eris):
    """Find first repeating layout during passing minutes on eris."""
    layouts = set()
    while (cur_layout := tuple(tuple(row) for row in eris)) not in layouts:
        layouts.add(cur_layout)
        eris = pass_minute(eris)
    return cur_layout


def pass_minute(eris):
    """Pass minute on eris."""
    grid = [row[:] for row in eris]
    for row_no, row in enumerate(eris):
        for col_no, tile in enumerate(row):
            adjacent_coordinates = get_adjacent_coordinates(row_no, col_no)
            adjacent_tiles = [
                eris[row][col] for row, col in adjacent_coordinates]
            adjacent_bug_count = adjacent_tiles.count(BUG)
            new_tile = get_new_tile(tile, adjacent_bug_count)
            if new_tile:
                grid[row_no][col_no] = new_tile
    return grid


@lru_cache()
def get_adjacent_coordinates(row, col):
    """Get possible adjacent coordinates for (row, col)."""
    adjacent = []
    for change_row, change_col in MOVES:
        next_row = row + change_row
        next_col = col + change_col
        if not ((0 <= next_row < 5) and (0 <= next_col < 5)):
            continue
        adjacent.append((next_row, next_col))
    return adjacent


def count_bugs(eris):
    """Count bugs on eris."""
    if isinstance(eris, list):
        return sum(row.count(BUG) for row in eris)
    return sum(count_bugs(eris_level) for eris_level in eris.values())


def count_biodiversity(eris):
    """Calculate biodiversity rating for eris."""
    rating = 0
    for row_no, row in enumerate(eris):
        for col_no, tile in enumerate(row):
            if tile != BUG:
                continue
            cur_power = row_no * 5 + col_no
            rating += 2**cur_power
    return rating


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
