"""Advent of Code 2018 Day 10."""
import re


LIGHT = '#'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    points = parse_points(lines)
    diverged_points, time_to_wait = diverge(points)
    placed = place_on_grid(diverged_points)
    print('Message:')
    for row in placed:
        print(''.join(row))
    print(f'Time to wait for message to appear: {time_to_wait}')


def diverge(points):
    """Diverge points."""
    seconds = 0
    while points_not_diverged(points, 165):
        for point in points:
            move_point(point)
        seconds += 1
    return points, seconds


def get_points_ranges(points):
    """Get minimum and maximum coordinate values of points."""
    ranges = []
    for coord in (0, 1):
        cur_coordinate = []
        for func in (min, max):
            cur_coordinate.append(func(
                points, key=lambda point: point['position'][coord]
            )['position'][coord])
        ranges.append(cur_coordinate)
    return ranges


def adjust_points(points, adjust_values):
    """Adjust points by the minimum coordinate values."""
    for point in points:
        point['position'] = [
            value - adjust
            for value, adjust in zip(point['position'], (adjust_values))]


def place_on_grid(points):
    """Place points on grid."""
    ranges = get_points_ranges(points)
    adjust_values = [maximum - minimum for minimum, maximum in ranges]
    grid = [['.' for _ in range(adjust_values[0] + 1)]
            for _ in range(adjust_values[1] + 1)]
    adjust_points(points, (ranges[0][0], ranges[1][0]))
    for point in points:
        cur_x, cur_y = point['position']
        grid[cur_y][cur_x] = LIGHT
    return grid


def move_point(point):
    """Move point by it velocity."""
    for index, change in enumerate(point['velocity']):
        point['position'][index] += change
    return point


def points_not_diverged(points, limit):
    """Check if all absolute point coordinates are below limit."""
    return any(
        any(abs(value) > limit for value in point['position'])
        for point in points
    )


def parse_points(lines):
    """Parse lines to points with position and velocity."""
    points = []
    for line in lines:
        position, velocity = [
            [int(num) for num in part.split(', ')]
            for part in re.findall(r'<(.*?)>', line)]
        points.append({'position': position, 'velocity': velocity})
    return points


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
