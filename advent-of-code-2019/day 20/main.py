"""Advent of Code 2019 Day 20."""
from collections import defaultdict, deque, namedtuple


WALL = '#'
PASSAGE = '.'
MOVES = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)
maze_path = namedtuple('maze', 'source target')


def main(file_input='input.txt'):
    grid = [line.rstrip('\n') for line in get_file_contents(file_input)]
    entries, *portals = parse_grid(grid)
    maze = maze_path(entries['AA'][0][0], entries['ZZ'][0][0])
    runs = (
        ('', False),
        (' on the outermost maze', True),
    )
    for description, recursive_level in runs:
        shortest = find_shortest_path(
            grid,
            portals,
            maze,
            levels=recursive_level)
        print(f'Shortest path from AA to ZZ tiles{description}: {shortest}')


def find_shortest_path(grid, portals, maze, start_level=0, levels=False):
    """Find shortest path on grid from maze.source to maze.target."""
    queue = deque()
    queue.append((maze.source, [], 0, start_level))
    visited = set()
    while queue:
        cur_move = queue.popleft()
        position, path, steps, level = cur_move
        if (not levels or level == 0) and position == maze.target:
            return steps
        if (position, level) in visited:
            continue
        visited.add((position, level))
        queue.extend(visit_position(
            grid, *portals, cur_move, maze, levels
        ))
    return None


def visit_position(grid, portals, portal_locations, cur_move, maze, levels):
    """Visit position on grid. Return list with allowed next moves"""
    position, path, steps, level = cur_move
    next_moves = []
    for move in MOVES:
        next_row, next_col = next_position = tuple([
            value + change
            for value, change in zip(position, move)])
        next_cell = grid[next_row][next_col]
        next_steps = steps + 1
        next_level = level
        next_path = path
        if next_cell != PASSAGE:
            continue
        is_outer_maze = next_position in set(maze) and level != 0
        if levels and is_outer_maze:
            continue
        if next_position in portals:
            name, level_change = portal_locations[next_position]
            changed_position, _ = portals[next_position]
            if levels and level == 0 and level_change == -1:
                continue
            next_steps += 1
            next_level += level_change
            next_position = changed_position
            next_path = next_path + [(name, next_level)]
        next_moves.append((next_position, next_path, next_steps, next_level))
    return next_moves


def parse_grid(grid):
    """Entries, portals and portal_locations from the grid."""
    entries = defaultdict(list)
    portal_locations = {}
    for row_no, row in enumerate(grid[2:-2], start=2):
        for col_no, col in enumerate(row[2:-2], start=2):
            if col != PASSAGE:
                continue
            if not (portal_name := check_portal(grid, row_no, col_no)):
                continue
            level_change = get_level_change(grid, row_no, col_no)
            entries[portal_name].append(((row_no, col_no), level_change))
            portal_locations[(row_no, col_no)] = portal_name, level_change
    portals = get_portals(entries)
    return entries, portals, portal_locations


def get_level_change(grid, row, col):
    """Get level change for (row, col) on grid."""
    if (row == 2
        or row == len(grid) - 3
        or col == 2
            or col == len(grid[0]) - 3):
        return -1
    return 1


def check_portal(grid, cur_row, cur_col):
    """Check if at (cur_row, cur_col) is portal."""
    changes = (
        (lambda row, col: is_portal(grid, ((row - 1, col), (row - 2, col))),
         lambda row, col: get_portal_name(grid,
                                          ((row - 2, col), (row - 1, col)))),
        (lambda row, col: is_portal(grid, ((row, col - 1), (row, col - 2))),
         lambda row, col: get_portal_name(grid,
                                          ((row, col - 2), (row, col - 1)))),
        (lambda row, col: is_portal(grid, ((row, col + 1), (row, col + 2))),
         lambda row, col: get_portal_name(grid,
                                          ((row, col + 1), (row, col + 2)))),
        (lambda row, col: is_portal(grid, ((row + 1, col), (row + 2, col))),
         lambda row, col: get_portal_name(grid,
                                          ((row + 1, col), (row + 2, col)))),
    )
    for check, get_name in changes:
        if check(cur_row, cur_col):
            return get_name(cur_row, cur_col)
    return False


def get_portal_name(lines, coordinates):
    """Get portal name for coordinates."""
    return ''.join(
        lines[row][col]
        for row, col in coordinates
    )


def is_portal(grid, coordinates):
    """Check coordinates for portal."""
    return all(
        grid[row][col].isalpha()
        for row, col in coordinates
    )


def get_portals(entries):
    """Create mapping of portal entrances from entries."""
    portals = {}
    for portal_name, locations in entries.items():
        if len(locations) == 2:
            (location1, level_change1), (location2, level_change2) = locations
            portals[location1] = location2, level_change2
            portals[location2] = location1, level_change1
    return portals


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
