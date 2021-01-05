"""Advent of Code 2015 Day 9."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    cities, distances = parse_distances(lines)
    paths = sorted(find_paths(cities, distances, 0, []))
    print(f'Shortest path: {paths[0]}')
    print(f'Longest path: {paths[-1]}')


def find_paths(cities_left, location_distances, total_distance, path):
    """Find possible paths between cities_left, with location_distances."""
    if len(cities_left) == 1:
        return [(total_distance, path)]
    paths = []
    source_cities = [path[-1]] if path else cities_left
    for city in source_cities:
        next_path = path if path else [city]
        next_cities = cities_left - {city}
        for target, distance in location_distances[city]:
            if target not in next_cities:
                continue
            paths.extend(find_paths(next_cities.copy(),
                                    location_distances,
                                    total_distance + distance,
                                    next_path + [target]))
    return paths


def parse_distances(lines):
    """Parse lines to cities set and distances between them dictionary."""
    cities = set()
    distances = defaultdict(list)
    for line in lines:
        source, target, distance = parse_distance(line)
        cities = cities | {source, target}
        distances[source].append((target, distance))
        distances[target].append((source, distance))
    return cities, distances


def parse_distance(line):
    """Parse line to tuple with source, target and distance."""
    cities, distance = line.split(' = ')
    source, target = cities.split(' to ')
    return source, target, int(distance)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
