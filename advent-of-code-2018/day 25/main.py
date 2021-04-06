"""Advent of Code 2018 Day 25."""
from collections import defaultdict


def main(file_input='input.txt'):
    points = [tuple(int(num) for num in line.strip().split(','))
              for line in get_file_contents(file_input)]
    constellations = find_constellations(points)
    print('Number of constellations formed by the points: '
          f'{len(constellations)}')


def find_constellations(points):
    """Find constellations among points."""
    constellations = defaultdict(set)
    point_to_constellation = {}
    constellation_no = 0
    for point in points:
        points_in_range = get_points_in_range(point, points)

        linked_constellations = get_linked_constellations(
            point_to_constellation, points_in_range)
        if not linked_constellations:
            linked_constellations.add(constellation_no)
            constellation_no += 1

        points_in_range.update(points_from_linked_constellations(
            linked_constellations, constellations))

        new_constelation = linked_constellations.pop()
        constellations[new_constelation] = points_in_range
        update_points_constellation(
            points_in_range, new_constelation, point_to_constellation)
        remove_linked_constellations(linked_constellations, constellations)
    return constellations


def points_from_linked_constellations(linked_constellations, constellations):
    """Get points from linked_constellations."""
    linked_points = set()
    for constellation in linked_constellations:
        linked_points = linked_points | constellations[constellation]
    return linked_points


def remove_linked_constellations(linked_constellations, constellations):
    """Remove linked_constellations from constellations."""
    for constellation in linked_constellations:
        del constellations[constellation]


def update_points_constellation(
        points_in_range, new_constelation, point_to_constellation):
    """Update point_to_constellation mapping for points_in_range."""
    for point_in_range in points_in_range:
        point_to_constellation[point_in_range] = new_constelation


def get_linked_constellations(point_to_constellation, points_in_range):
    """Get constellations to which are connected points_in_range."""
    linked_constellations = set()
    for point_in_range in points_in_range:
        constellation = point_to_constellation.get(point_in_range)
        if constellation is not None:
            linked_constellations.add(constellation)
    return linked_constellations


def get_points_in_range(point, points):
    """Get points in range of point."""
    in_range = {point}
    for other_point in points:
        if is_in_range(point, other_point):
            in_range.add(other_point)
    return in_range


def is_in_range(point, other_point, distance=3):
    """Check if point and other_point are within wanted distance."""
    points_distance = sum(
        abs(coord1 - coord2)
        for coord1, coord2 in zip(point, other_point))
    return points_distance <= distance


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
