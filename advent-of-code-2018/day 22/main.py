"""Advent of Code 2018 Day 22."""
import heapq


ROCKY = '.'
WET = '='
NARROW = '|'
MOUTH = 'M'
TARGET = 'T'

NEITHER = 0
TORCH = 1
GEAR = 2

TYPE_TO_RISK = {
    ROCKY: 0,
    WET: 1,
    NARROW: 2,
}
EROSION_TO_TYPE = {
    0: ROCKY,
    1: WET,
    2: NARROW
}
MOVES = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
)
REGION_TO_TOOLS = {
    ROCKY: {GEAR, TORCH},
    WET: {GEAR, NEITHER},
    NARROW: {TORCH, NEITHER},
    'M': {TORCH},
    'T': {TORCH}
}

example_depth = 510
example_target = (10, 10)


def main(file_input='input.txt'):
    depth_line, target_line = [
        line.strip() for line in get_file_contents(file_input)]
    depth = int(depth_line.split(': ')[1])
    target = tuple([
        int(coordinate)
        for coordinate in target_line.split(': ')[1].split(',')][::-1])
    cave = [[None for _ in range(target[1] + 1)]
            for _ in range(target[0] + 1)]
    filled = fill_cave(cave, depth, target)
    risk = count_risk(filled, target)
    print('Total risk level of smallest rectangle including '
          f'(0, 0) and {target}: {risk}')
    fastest_way = find_fastest_way(depth, target)
    print(f'Fewest number of minutes to reach target: {fastest_way}')


def find_fastest_way(depth, target):
    """Find fastest way to the target, in cave with depth number."""
    heap = []
    heapq.heappush(heap, (0, 0, 0, TORCH))
    visited = {((0, 0), TORCH): 0}
    while True:
        cur_parameters = heapq.heappop(heap)
        cur_time, cur_row, cur_col, cur_tool = cur_parameters
        if (cur_row, cur_col) == target and cur_tool == TORCH:
            return cur_time
        next_time = cur_time + 1
        next_parameters = next_time, cur_row, cur_col, cur_tool
        next_moves = get_next_moves(next_parameters, depth, target)
        next_time += 7
        cur_type = get_type(cur_row, cur_col, depth, target)
        for next_tool in REGION_TO_TOOLS[cur_type] - {cur_type}:
            next_parameters = next_time, cur_row, cur_col, next_tool
            next_moves.extend(get_next_moves(next_parameters, depth, target))
        visit(validate_moves(next_moves, depth, target), visited, heap)


def visit(next_moves, visited, heap):
    """Visits next_moves if their target doesn't have already faster way."""
    for next_parameters in next_moves:
        next_time, next_row, next_col, next_tool = next_parameters
        next_params = ((next_row, next_col), next_tool)
        if (visited.get(next_params, float('inf')) <= next_time):
            continue
        visited[next_params] = next_time
        heapq.heappush(heap, next_parameters)


def validate_moves(moves, depth, target):
    valid_moves = []
    for move_parameters in moves:
        next_time, next_row, next_col, next_tool = move_parameters
        if next_row < 0 or next_col < 0:
            continue
        next_type = get_type(next_row, next_col, depth, target)
        if not is_tool_allowed(next_type, next_tool):
            continue
        valid_moves.append(move_parameters)
    return valid_moves


def get_next_moves(move_parameters, depth, target):
    """Get next moves based on the parameters."""
    next_time, cur_row, cur_col, next_tool = move_parameters
    next_moves = []
    for row_change, col_change in MOVES:
        next_row = cur_row + row_change
        next_col = cur_col + col_change
        if next_row < 0 or next_col < 0:
            continue
        next_type = get_type(next_row, next_col, depth, target)
        if not is_tool_allowed(next_type, next_tool):
            continue
        next_moves.append((next_time, next_row, next_col, next_tool))
    return next_moves


def is_tool_allowed(region_type, tool):
    """Check if tool is allowed in region_type."""
    return tool in REGION_TO_TOOLS[region_type]


def count_risk(cave, target):
    """Count total risk for the cave up to target."""
    counter = 0
    rows, cols = target
    for row in range(rows + 1):
        for col in range(cols + 1):
            counter += TYPE_TO_RISK.get(cave[row][col], 0)
    return counter


def fill_cave(cave, depth, target):
    """Fill cave with depth number and up to target."""
    rows, cols = target
    for row in range(rows + 1):
        for col in range(cols + 1):
            if row == 0 and col == 0:
                region_type = MOUTH
            elif [row, col] == target:
                region_type = TARGET
            else:
                region_type = get_type(row, col, depth, target)
            cave[row][col] = region_type
    cave[rows][cols] = TARGET
    return cave


def get_type(row, col, depth, target):
    """Get region type of (row, col)."""
    if (row, col) == target:
        return TARGET
    return EROSION_TO_TYPE[get_erosion_level(row, col, depth, target) % 3]


def get_erosion_level(row, col, depth, target, memo={}):
    """Get erosion level of the (row, col)."""
    if (row, col) in memo:
        return memo[(row, col)]
    result = (get_geologic_index(row, col, depth, target) + depth) % 20183
    memo[(row, col)] = result
    return result


def get_geologic_index(row, col, depth, target, memo={}):
    """Get geologic index of the (row, col)."""
    if (row == 0 and col == 0) or (row, col) == target:
        result = 0
    elif row == 0:
        result = col * 16807
    elif col == 0:
        result = row * 48271
    else:
        result = (get_erosion_level(row, col - 1, depth, target)
                  * get_erosion_level(row - 1, col, depth, target))
    memo[(row, col)] = result
    return result


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
