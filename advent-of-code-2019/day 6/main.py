"""Advent of Code 2019 Day 6."""
from collections import defaultdict


COM = 'COM'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    orbits, orbiting = parse_orbits(lines)
    orbit_count = count_orbits(orbits, COM, 0)
    print(f'Number of direct and indirect orbits in data: {orbit_count}')
    transfers = find_transfer(orbiting, 'YOU', 'SAN')
    print(f'Minimum number of transfers to move from YOU to SAN: {transfers}')


def find_transfer(orbiting, source, target):
    """Find minimum number of transfers from source to target."""
    source_way, target_way = [
        find_way_from(orbiting, cur_object) for cur_object in (source, target)]
    while ways_have_matching_objects(source_way, target_way):
        source_way.pop()
        target_way.pop()
    return len(source_way) + len(target_way)


def ways_have_matching_objects(way1, way2):
    """Check if way1 and way2 have matching objects in path."""
    return way1[-1] == way2[-1]


def find_way_from(orbiting, source):
    """Find way from source to COM."""
    way = []
    orbit = source
    while orbit != COM:
        orbit = orbiting[orbit]
        way.append(orbit)
    return way


def count_orbits(orbits, cur_object, cur_orbit):
    """Count direct and indirect orbits, starting from cur_object."""
    if not orbits[cur_object]:
        return cur_orbit
    return sum(count_orbits(orbits, next_object, cur_orbit + 1)
               for next_object in orbits[cur_object]) + cur_orbit


def parse_orbits(lines):
    """Parse lines to orbits and orbiting dictionaries."""
    orbiting = {}
    orbits = defaultdict(list)
    for line in lines:
        name, orbited_by = line.split(')')
        orbits[name].append(orbited_by)
        orbiting[orbited_by] = name
    return orbits, orbiting


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
