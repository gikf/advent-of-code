"""Advent of Code 2019 Day 10."""
from collections import defaultdict
import math


EMPTY = '.'
ASTEROID = '#'


def main(file_input='input.txt'):
    grid = [line.strip() for line in get_file_contents(file_input)]
    count, best_point = find_best_location(grid)
    print(f'Asteroids detected from best location: {count}')
    angles = find_angles_from_point(grid, *best_point)
    angles = {
        angle % 360 if angle < -90 else angle: points
        for angle, points in angles.items()}
    destroy_list = destroy_asteroids(angles)
    _, (_, (coord_y, coord_x)) = destroy_list[199]
    value = coord_x * 100 + coord_y
    print(f'Value of asteroid destroyed as 200th: {value}')


def destroy_asteroids(angles):
    """Destroy asteroids, start with laser pointing up and rotate clockwise."""
    destroy_list = []
    sorted_angles = sorted(angles)
    while sorted_angles:
        for angle in sorted_angles:
            if not angles[angle]:
                sorted_angles.remove(angle)
            else:
                asteroids = sorted(angles[angle])
                to_remove = asteroids[0]
                angles[angle].remove(to_remove)
                destroy_list.append((angle, to_remove))
    return destroy_list


def find_angles_from_point(grid, row, col):
    """Find angles to asteroids on grids from (row, col)."""
    angles = defaultdict(list)
    for row_no, cur_row in enumerate(grid):
        for col_no, cell in enumerate(cur_row):
            if cell != ASTEROID or (row, col) == (row_no, col_no):
                continue
            row_aligned = row_no - row
            col_aligned = col_no - col
            angle = math.atan2(row_aligned, col_aligned) * 180 / math.pi
            distance = (row_aligned**2 + col_aligned**2)**0.5
            angles[angle].append((distance, (row_no, col_no)))
    return angles


def find_best_location(grid):
    """Find best location - detecting the most asteroids - for grid."""
    counts = []
    for row_no, row in enumerate(grid):
        for col_no, cell in enumerate(row):
            if cell != ASTEROID:
                continue
            counts.append(
                (len(find_angles_from_point(grid, row_no, col_no)),
                 (row_no, col_no)))
    return max(counts)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
