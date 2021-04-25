"""Advent of Code 2019 Day 18."""
from collections import deque
from heapq import heappop, heappush


WALL = '#'
PASSAGE = '.'
ENTRANCE = '@'
MOVES = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)
DOOR = object()
KEY = object()


def main(file_input='input.txt'):
    grid = [[*line.strip()] for line in get_file_contents(file_input)]
    locations, keys, entrance = parse_grid(grid)
    shortest_path = find_shortest_path(
        grid, keys, entrance.pop(), locations)
    print(f'Steps in shortest path to collect all keys: {shortest_path}')
    grid[39][39:42] = ['@', '#', '@']
    grid[40][39:42] = ['#', '#', '#']
    grid[41][39:42] = ['@', '#', '@']
    locations, keys, entrances = parse_grid(grid)
    entrances = tuple(position for _, position in entrances)
    fewest = find_shortest_path_with_4_robots(grid, entrances, '')
    print(f'Steps to collect all keys using four robots: {fewest}')


def find_paths(grid, entrance, keys_left):
    """Find paths on grid, starting from entrance."""
    queue = deque([entrance])
    distance = {entrance: 0}
    keys = {}
    while queue:
        location = queue.popleft()
        for move in MOVES:
            next_row, next_col = [
                value + change for value, change in zip(location, move)]
            cur_cell = grid[next_row][next_col]
            if cur_cell == WALL or (next_row, next_col) in distance:
                continue
            distance[(next_row, next_col)] = distance[location] + 1
            if cur_cell.isupper() and cur_cell.lower() not in keys_left:
                continue
            if cur_cell.islower() and cur_cell not in keys_left:
                keys[cur_cell] = (
                    distance[(next_row, next_col)], (next_row, next_col))
            else:
                queue.append((next_row, next_col))
    return keys


def find_distances(grid, entrances, keys_left):
    """Find distances on grid to keys"""
    keys = {}
    for index, entrance in enumerate(entrances):
        paths = find_paths(grid, entrance, keys_left).items()
        for cur_cell, (distance, location) in paths:
            keys[cur_cell] = distance, location, index
    return keys


def find_shortest_path_with_4_robots(grid, entrances, keys_left, seen={}):
    """Find shortest path on grid to collect all keys, using four robots."""
    seen_key = ''.join(sorted(keys_left))
    if (entrances, seen_key) in seen:
        return seen[entrances, seen_key]
    keys = find_distances(grid, entrances, keys_left)
    if len(keys) == 0:
        result = 0
    else:
        distances = []
        for cur_cell, (distance, location, entrance_index) in keys.items():
            cur_entrance = tuple(
                location if index == entrance_index else entrance
                for index, entrance in enumerate(entrances))
            distances.append(
                distance + find_shortest_path_with_4_robots(
                    grid, cur_entrance, keys_left + cur_cell)
            )
        result = min(distances)
    seen[entrances, seen_key] = result
    return result


def find_shortest_path(grid, keys, entrance, locations):
    """Find shortest path on grid to collect keys."""
    queue = deque()
    queue = [(0, [entrance], keys)]
    best = float('inf')
    seen = {}
    while queue:
        steps, path, keys_left = heappop(queue)
        if best < steps:
            break
        cur_cell, cur_location = path[-1]
        seen_key = (tuple(sorted(keys_left)), cur_location)
        if seen_key in seen:
            best_steps, best_keys = seen[seen_key]
            if best_steps < steps:
                continue
        else:
            seen[seen_key] = steps, tuple(sorted(keys_left))
        if not keys_left:
            return steps
        distances_from = find_distances_from(
            grid, *cur_location, keys_left)
        for next_cell, values in distances_from.items():
            distance, (next_row, next_col), needed_keys = values
            if (next_cell == ENTRANCE
                or next_cell not in keys_left
                    or needed_keys & keys_left):
                continue
            heappush(
                queue, (
                    steps + distance,
                    path + [(next_cell, locations[next_cell])],
                    keys_left - {next_cell},
                )
            )
    return None


def find_distances_from(grid, row, col, keys=None, memo={}):
    """Find distances on grid from (row, col)."""
    if len(memo) > 3000:
        memo.clear()
    memo_key = (row, col, tuple(sorted(keys)))
    if memo_key in memo:
        return memo[memo_key]
    distances = {}
    queue = deque()
    queue.append(((row, col), 0, set()))
    visited = set()
    while queue:
        cur_location, steps, needed_keys = queue.popleft()
        if cur_location in visited:
            continue
        visited.add(cur_location)
        cur_row, cur_col = cur_location
        cur_cell = grid[cur_row][cur_col]
        if cur_cell.islower() and cur_location != (row, col):
            distances[cur_cell] = (
                steps, (cur_row, cur_col), needed_keys.copy())
        if cur_cell.islower():
            needed_keys = needed_keys | {cur_cell.lower()}
        for move in MOVES:
            next_row, next_col = [
                value + change
                for value, change in zip(cur_location, move)]
            next_cell = grid[next_row][next_col]
            if keys and next_cell.isupper() and next_cell.lower() in keys:
                continue
            if next_cell == WALL:
                continue
            queue.append(((next_row, next_col), steps + 1, needed_keys))
    memo[memo_key] = distances
    return distances


def parse_grid(grid):
    """Parse grid to keys, locations and entrances."""
    keys = set()
    locations = {}
    entrances = set()
    for row_no, row in enumerate(grid):
        for col_no, col in enumerate(row):
            if col in set((WALL, PASSAGE)):
                continue
            position = (row_no, col_no)
            if col == ENTRANCE:
                entrances.add((col, position))
                locations[col] = position
            elif col.islower():
                keys.add(col)
                locations[col] = position
    return locations, keys, entrances


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
