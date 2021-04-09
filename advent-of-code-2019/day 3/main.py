"""Advent of Code 2019 Day 3."""


DIRECTIONS = {
    'L': (0, -1),
    'R': (0, 1),
    'U': (1, 0),
    'D': (-1, 0),
}


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    wires = parse_wires(lines)
    wire_points = [follow_wire(wire) for wire in wires]
    (wire1, _), (wire2, _) = wire_points
    intersections = wire1 & wire2
    distances_to_intersection = [
        get_distance(point, (0, 0)) for point in intersections]
    shortest_distance = sorted(distances_to_intersection)[0]
    print(f'Distance to closest intersection: {shortest_distance}')
    combined_steps = [sum(steps[point] for _, steps in wire_points)
                      for point in intersections]
    fewest_steps = sorted(combined_steps)[0]
    print(f'Fewest combined steps to reach intersection: {fewest_steps}')


def follow_wire(wire):
    """Follow wire, return wire points and mapping to step reaching it."""
    points = set()
    point_to_step_number = {}
    total_steps = 1
    cur_position = (0, 0)
    for direction, steps in wire:
        changes = DIRECTIONS[direction]
        for _ in range(steps):
            cur_position = tuple(
                coordinate + change
                for coordinate, change in zip(cur_position, changes))
            points.add(cur_position)
            if cur_position not in point_to_step_number:
                point_to_step_number[cur_position] = total_steps
            total_steps += 1
    return points, point_to_step_number


def parse_wires(lines):
    """Parse lines to wires."""
    return [parse_wire(line) for line in lines]


def parse_wire(line):
    """Parse line to directions with steps creating wire."""
    wire = []
    for instruction in line.split(','):
        direction, *steps = instruction
        wire.append((direction, int(''.join(steps))))
    return wire


def get_distance(source, target):
    """Get Manhattan distance between points source and target."""
    return sum(abs(val1 - val2) for val1, val2 in zip(source, target))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
