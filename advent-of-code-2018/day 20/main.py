"""Advent of Code 2018 Day 20."""
from collections import deque


WALL = '#'
DOOR_H = '-'
DOOR_V = '|'
UNKNOWN = '?'
ROOM = '.'
START = 'X'
MOVES = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)
DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'W': (0, -1),
    'S': (1, 0)
}
DIRECTION_TO_DOOR = {
    'N': DOOR_H,
    'S': DOOR_H,
    'E': DOOR_V,
    'W': DOOR_V,
}


def main(file_input='input.txt'):
    regex = get_file_contents(file_input)[0].strip()
    start = [[UNKNOWN for _ in range(3)]
             for _ in range(3)]
    start[1][1] = START
    facility = build_facility(regex, start)
    moves_start = find_start(facility)
    distances = find_distances(facility, moves_start)
    furthest_room = find_furthest_room(distances)
    print('Number of doors to pass through to reach furthest room: '
          f'{furthest_room}')
    at_least_1000_doors_between = find_rooms_at_least_far_as(distances, 1000)
    print('Rooms with shortest path needing to pass through at least 1000 '
          f'doors: {at_least_1000_doors_between}')


def find_rooms_at_least_far_as(distances, wanted_distance):
    """Find rooms with at least wanted_distance from the distances grid."""
    return sum(
        True
        for row in distances
        for col in row
        if col > 0 and col >= wanted_distance
    )


def find_furthest_room(distances):
    """Find furthest room from the distances grid."""
    return max(max(row) for row in distances)


def find_distances(facility, start):
    """Find distances from start to different rooms in facility."""
    distances = [[float('-inf') for _ in range(len(facility[0]))]
                 for _ in range(len(facility))]
    cur_row, cur_col = start
    distances[cur_row][cur_col] = 0
    queue = deque()
    visited = set()
    queue.append((cur_row, cur_col))

    while queue:
        cur_room = queue.popleft()
        if cur_room in visited:
            continue
        visited.add(cur_room)

        row, col = cur_room
        cur_distance = distances[row][col]
        if facility[row][col] in {DOOR_H, DOOR_V}:
            distances[row][col] = -1

        for change in MOVES:
            next_row, next_col = [value + change
                                  for value, change in zip(cur_room, change)]
            next_cell = facility[next_row][next_col]
            next_distance = cur_distance
            if next_cell in {START, WALL} or (next_row, next_col) in visited:
                continue
            elif next_cell not in {DOOR_H, DOOR_V}:
                next_distance = cur_distance + 1
            distances[next_row][next_col] = next_distance
            queue.append((next_row, next_col))
    return distances


def find_start(facility):
    """Find starting position in facility."""
    for row_no, row in enumerate(facility):
        for col_no, col in enumerate(row):
            if col == START:
                return row_no, col_no
    return None


def build_facility(regex, facility):
    """Build facility based on regex."""
    cur_position = find_start(facility)
    stack = []
    for char in regex:
        if char == '(':
            stack.append(cur_position)
        elif char == '|':
            cur_position = stack[-1]
        elif char == ')':
            cur_position = stack.pop()
        if char in {'^', '$', '(', ')', '|'}:
            continue
        row, col = cur_position
        row_change, col_change = DIRECTIONS[char]
        next_row = row + row_change
        next_col = col + col_change
        if does_need_adjust(row_change, next_row, len(facility)):
            change, facility = expand_grid(facility, char)
            row += change
            stack = [(row + change, col) for row, col in stack]
        if does_need_adjust(col_change, next_col, len(facility[0])):
            change, facility = expand_grid(facility, char)
            col += change
            stack = [(row, col + change) for row, col in stack]
        cur_position = move_position(facility, (row, col), char)
    change_unknown_to_walls(facility)
    return facility


def does_need_adjust(change, next_value, limit):
    """Check if change of the next_value will need adjust."""
    return change and (next_value - 1 < 0 or next_value + 1 >= limit)


def change_unknown_to_walls(facility):
    """Changes unknown cells to walls."""
    for row_no, row in enumerate(facility):
        for col_no, col in enumerate(row):
            if col in UNKNOWN:
                facility[row_no][col_no] = WALL


def move_position(facility, cur_position, direction):
    """Move position from cur_position in the direction on facility."""
    changes = DIRECTIONS[direction]
    doors = DIRECTION_TO_DOOR[direction]
    for cell in (doors, ROOM):
        next_position = []
        for coordinate, change in zip(cur_position, changes):
            next_position.append(coordinate + change)
        row, col = next_position
        facility[row][col] = cell
        cur_position = next_position
    return row, col


def expand_grid(grid, direction):
    """Expand grid depending on direction."""
    row, col = DIRECTIONS[direction]
    if row == -1:
        new_rows = [[UNKNOWN for _ in range(len(grid[0]))]
                    for _ in range(2)]
        return 2, new_rows + grid
    elif row == 1:
        new_rows = [[UNKNOWN for _ in range(len(grid[0]))]
                    for _ in range(2)]
        return 0, grid + new_rows
    elif col == -1:
        return 2, [[UNKNOWN for _ in range(2)] + cur_row for cur_row in grid]
    elif col == 1:
        return 0, [cur_row + [UNKNOWN for _ in range(2)] for cur_row in grid]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
