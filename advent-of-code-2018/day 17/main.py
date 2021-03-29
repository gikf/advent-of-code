"""Advent of Code 2018 Day 17."""
from collections import deque
import re


CLAY = '#'
SAND = '.'
WATER = '|'
REST_WATER = '~'
SPRING = '+'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    clays = parse_clays(lines)
    boundaries = get_boundaries(clays)
    bound_x, bound_y = boundaries
    adjusted_clays = adjust_clays(clays, bound_x[0], bound_y[0])
    columns, rows = [maximum - minimum for minimum, maximum in boundaries]
    grid = [[SAND for _ in range(columns + 3)]
            for _ in range(rows + 2)]
    fill_grid(grid, adjusted_clays)
    grid[0][500 - bound_x[0]] = SPRING
    flow_water(grid, (0, 500 - bound_x[0]))
    water = count_water(grid)
    print(f'Number of tiles water can reach: {water}')
    retained_water = count_retained(grid)
    print(f'Number of water left after running dry: {retained_water}')


def flow_water(grid, spring):
    """Flow water from spring."""
    queue = deque()
    queue.append(spring)
    rows = len(grid)
    columns = len(grid[0])
    while queue:
        cur_square = queue.popleft()
        cur_row, cur_col = cur_square
        if cur_row + 1 >= rows or cur_col + 1 >= columns:
            continue
        if can_water_flow_down(grid, cur_square):
            grid[cur_row + 1][cur_col] = WATER
            queue.append((cur_row + 1, cur_col))
        elif is_bowl(grid, cur_square):
            fill_bowl(grid, cur_square, queue)
        elif is_water_splashing(grid, cur_row, cur_col):
            splash_water(grid, cur_square, queue)


def fill_bowl(grid, cur_square, queue):
    """Fill on grid bowl having cur_square."""
    cur_row, cur_col = cur_square
    next_row = cur_row - 1
    fill_bowl_level(grid, cur_square)
    if is_bowl(grid, (next_row, cur_col)):
        if is_bowl_level_watered(grid, (next_row, cur_col)):
            grid[next_row][cur_col] = WATER
            queue.append((next_row, cur_col))
    else:
        splash_water(grid, (next_row, cur_col), queue)


def is_water_splashing(grid, cur_row, cur_col):
    """Check if water is splashing to left and right at (cur_row, cur_col)."""
    return (grid[cur_row + 1][cur_col] == CLAY
            and grid[cur_row][cur_col] == WATER
            and grid[cur_row][cur_col - 1] != WATER
            and grid[cur_row][cur_col + 1] != WATER)


def splash_water(grid, cur_square, queue):
    """Let water to splash to left and right until flows down."""
    cur_row, cur_col = cur_square
    go_left = cur_col
    while 0 <= go_left and grid[cur_row][go_left] != CLAY:
        grid[cur_row][go_left] = WATER
        if can_water_flow_down(grid, (cur_row, go_left)):
            queue.append((cur_row, go_left))
            break
        go_left -= 1
    go_right = cur_col + 1
    while go_right < len(grid[0]) and grid[cur_row][go_right] != CLAY:
        grid[cur_row][go_right] = WATER
        if can_water_flow_down(grid, (cur_row, go_right)):
            queue.append((cur_row, go_right))
            break
        go_right += 1


def fill_bowl_level(grid, cur_square):
    """Fill level of bowl."""
    cur_row, cur_col = cur_square
    go_left = cur_col
    while 0 <= go_left and grid[cur_row][go_left] != CLAY:
        grid[cur_row][go_left] = REST_WATER
        go_left -= 1
    go_right = cur_col + 1
    while go_right < len(grid[0]) and grid[cur_row][go_right] != CLAY:
        grid[cur_row][go_right] = REST_WATER
        go_right += 1


def is_bowl_level_watered(grid, cur_square):
    """Check if higher bowl is in watered part of bowl."""
    cur_row, cur_col = cur_square
    go_left = cur_col
    while 0 <= go_left and grid[cur_row][go_left] != CLAY:
        if grid[cur_row][go_left] in (WATER, REST_WATER):
            return True
        go_left -= 1
    go_right = cur_col + 1
    while go_right < len(grid[0]) and grid[cur_row][go_right] != CLAY:
        if grid[cur_row][go_right] in (WATER, REST_WATER):
            return True
        go_right += 1
    return False


def is_bowl(grid, cur_square):
    """Check if cur_square is within a bowl."""
    cur_row, cur_col = cur_square
    go_left = cur_col
    while (0 <= go_left
           and grid[cur_row][go_left] in (SAND, WATER, REST_WATER)):
        if can_water_flow_down(grid, (cur_row, go_left)):
            return False
        go_left -= 1
    go_right = cur_col + 1
    while (go_right < len(grid[0])
           and grid[cur_row][go_right] in (SAND, WATER, REST_WATER)):
        if can_water_flow_down(grid, (cur_row, go_right)):
            return False
        go_right += 1
    return True


def can_water_flow_down(grid, cur_square):
    """Check if water can flow further down."""
    row, col = cur_square
    next_row = row + 1
    if len(grid) <= next_row:
        return False
    if grid[next_row][col] in (SAND, WATER):
        return True
    return False


def fill_grid(grid, clays):
    """Fill grid with clays."""
    axises = {
        'x': get_coordinates,
        'y': lambda values, other: [
            result[::-1] for result in get_coordinates(values, other)],
    }
    for axis, [axis_value, *other_values] in clays:
        coordinates = axises[axis]
        for column, row in coordinates(axis_value, other_values):
            grid[row][column] = CLAY
    return grid


def get_coordinates(axis_value, ranges):
    """Get coordinates pairs from axis_value and other_values."""
    start, end = ranges
    return [(axis_value, other_value) for other_value in range(start, end + 1)]


def adjust_clays(clays, minimum_x, minimum_y):
    """Adjust clays coordinates with minimum_x and minimum_y."""
    adjusted = []
    axises = {
        'x': (minimum_x, minimum_y),
        'y': (minimum_y, minimum_x),
    }
    for clay in clays:
        axis, [axis_value, *other_values] = clay
        cur_values = []
        axis_minimum, other_minimum = axises[axis]
        cur_values.append(axis_value - axis_minimum + 1)
        cur_values.extend(value - other_minimum + 1 for value in other_values)
        adjusted.append((axis, cur_values))
    return adjusted


def get_boundaries(clays):
    """Get coordinates boundaries for grid from clays."""
    xes = []
    yes = []
    axises = {
        'x': (xes, yes),
        'y': (yes, xes),
    }
    for clay in clays:
        axis, [axis_value, *other_values] = clay
        first, second = axises[axis]
        first.append(axis_value)
        second.extend(other_values)
    return [(min(values), max(values)) for values in (xes, yes)]


def count_water(grid):
    """Count number of squares to which water is reaching."""
    return sum(row.count(WATER) + row.count(REST_WATER) for row in grid)


def count_retained(grid):
    """Count number of squares with retained water."""
    return sum(row.count(REST_WATER) for row in grid)


def parse_clays(lines):
    """Parse clays."""
    clays = []
    for line in lines:
        cur_clay = parse_clay(line)
        clays.append(cur_clay)
    return clays


def parse_clay(line):
    """Parse clay coordinates."""
    regex = r'(\w)=(\d+), \w=(\d+)..(\d+)'
    axis, *nums = re.findall(regex, line)[0]
    return (axis, [int(num) for num in nums])


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
