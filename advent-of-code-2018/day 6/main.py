"""Advent of Code 2017 Day 6."""
from collections import defaultdict, deque


EQUAL = '.'


def main(file_input='input.txt'):
    points = [[int(num)
              for num in line.strip().split(', ')]
              for line in get_file_contents(file_input)]
    grid_edges = get_grid_edges(points)
    (min_x, max_x), (min_y, max_y) = grid_edges
    adjusted_points = adjust_points(points, min_x, min_y)
    adjusted_max = [top - low for low, top in grid_edges]
    grid = get_grid(*adjusted_max)
    distances_grid = get_closest_points(grid, adjusted_points)
    non_infinite_areas = sorted(
        get_non_infinite(distances_grid, points), reverse=True)
    print(non_infinite_areas[0])
    locations = get_locations_with_total_distance_less_than(
        adjusted_points, 10000, tuple([num // 2 for num in adjusted_max]))
    print(locations)


def get_grid_edges(points):
    """Get edges of grid containing all points."""
    grid_edges = []
    for index in range(2):
        point = []
        for func in (min, max):
            funciest_point = func(points, key=lambda item: item[index])
            point.append(func(funciest_point))
        grid_edges.append(point)
    return grid_edges


def get_locations_with_total_distance_less_than(points, limit, start):
    """Get locations count having total distance to points less than limit."""
    queue = deque([start])
    locations = set()
    area_size = 0
    while queue:
        cur_location = queue.popleft()
        if cur_location in locations:
            continue
        if get_total_distance(cur_location, points) >= limit:
            continue
        area_size += 1
        locations.add(cur_location)
        queue.extend(get_next_locations(*cur_location))
    return area_size


def get_next_locations(cur_x, cur_y):
    """Get next locations from (cur_x, cur_y) location."""
    changes = (
        (-1, 0),
        (1, 0),
        (0, 1),
        (0, -1),
    )
    return [(cur_x + change_x, cur_y + change_y)
            for change_x, change_y in changes]


def get_total_distance(location, points):
    """Get total distance from location to points."""
    return sum(get_distance(location, point) for point in points)


def get_non_infinite(grid, points):
    """Get size of areas on grid, which are finite."""
    on_edges = set()
    on_edges = on_edges | set(grid[0]) | set(grid[-1])
    for row in grid:
        on_edges.add(row[0])
        on_edges.add(row[-1])
    areas = []
    for index, point in enumerate(points):
        if index in on_edges:
            continue
        areas.append(count_occurences(grid, index))
    return areas


def count_occurences(grid, number):
    """Count occurrences of number on grid."""
    return sum(row.count(number) for row in grid)


def get_closest_points(grid, points):
    """Get on grid closest point from every cell."""
    for row_no, row in enumerate(grid):
        for col_no, col in enumerate(row):
            distances = defaultdict(list)
            for index, point in enumerate(points):
                distance = get_distance((row_no, col_no), point)
                distances[distance].append(index)
            minimum_distance = min(distances)
            if len(distances[minimum_distance]) == 1:
                grid[row_no][col_no] = distances[minimum_distance][0]
    return grid


def get_grid(columns, rows):
    """Get grid with size (rows, columns)."""
    return [[EQUAL for _ in range(columns)] for _ in range(rows)]


def adjust_points(points, adjust_x, adjust_y):
    """Adjust points based by adjust_x and adjust_y."""
    adjusted = []
    for point_x, point_y in points:
        adjusted.append((point_x - adjust_x, point_y - adjust_y))
    return adjusted


def get_distance(source, target):
    """Get Manhattan distance from source to target."""
    return sum(abs(num1 - num2) for num1, num2 in zip(source, target))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
