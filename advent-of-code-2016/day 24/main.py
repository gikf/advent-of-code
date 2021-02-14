"""Advent of Code 2016 Day 24."""
from collections import defaultdict, deque

EMPTY = '.'
WALL = '#'
MOVES = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
)


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    ducts, targets = parse_ducts(lines)
    distances = get_distances(targets, ducts)
    routes = get_routes([*range(1, len(targets))], [])
    routes_with_total_distance = [(count_route_distance(route, distances),
                                   [0] + route)
                                  for route in routes]
    sorted_routes = sorted(routes_with_total_distance)
    print(f'Shortest route: {sorted_routes[0]}')
    routes_ending_at_0 = [append_step_to_route(route, distances, 0)
                          for route in routes_with_total_distance]
    sorted_routes_ending_at_0 = sorted(routes_ending_at_0)
    print('Shortest route with step coming back to 0: '
          f'{sorted_routes_ending_at_0[0]}')


def append_step_to_route(route_with_distance, distances, next_step):
    """Append step to route_with_distance and update distance."""
    distance, route = route_with_distance
    return (distance + distances[route[-1]][next_step],
            route + [next_step])


def count_route_distance(route, distances):
    """Count distance of route based on distances between targets."""
    total_distance = 0
    source = 0
    for target in route:
        total_distance += distances[source][target]
        source = target
    return total_distance


def get_routes(targets_left, cur_route):
    """Get possible routes from targets_left."""
    if not targets_left:
        return [cur_route]
    routes = []
    for target in targets_left:
        next_left = targets_left[:]
        next_left.remove(target)
        routes.extend(get_routes(next_left, cur_route + [target]))
    return routes


def get_distances(targets, ducts):
    """Get distances in ducts between targets."""
    distances = defaultdict(dict)
    for target, (row, col) in targets:
        distances[target] = find_distances_from(ducts, row, col, len(targets))
    return distances


def find_distances_from(ducts, row, col, targets_count):
    """Find distances in ducts from row and col to targets_count targets."""
    distance_grid = get_grid(len(ducts), len(ducts[0]))
    visited = set()
    distances = {}
    queue = deque([(row, col)])
    while queue and len(distances) < targets_count - 1:
        cur_position = queue.popleft()
        cur_row, cur_col = cur_position
        if cur_position in visited:
            continue
        visited.add(cur_position)
        duct = ducts[cur_row][cur_col]
        cur_distance = distance_grid[cur_row][cur_col]
        if duct not in (EMPTY, WALL) and (row, col) != cur_position:
            distances[int(duct)] = cur_distance
        for move in get_next_moves(ducts, cur_row, cur_col):
            if move in visited:
                continue
            next_row, next_col = move
            distance_grid[next_row][next_col] = cur_distance + 1
            queue.append(move)
    return distances


def get_next_moves(ducts, row, col):
    """Get next moves in ducts from row and col."""
    moves = []
    for row_change, col_change in MOVES:
        next_row = row + row_change
        next_col = col + col_change
        if ducts[next_row][next_col] != WALL:
            moves.append((next_row, next_col))
    return moves


def get_grid(rows, cols):
    """Create grid with number of rows and cols."""
    return [[0 for _ in range(cols)]
            for _ in range(rows)]


def parse_ducts(lines):
    """Parse ducts to grid and set of targets."""
    targets = set()
    ducts = []
    for row_no, line in enumerate(lines):
        ducts.append(list(line))
        for col_no, cell in enumerate(line):
            if cell not in (EMPTY, WALL):
                targets.add((int(cell), (row_no, col_no)))
    return ducts, targets


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
