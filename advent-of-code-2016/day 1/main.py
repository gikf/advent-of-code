"""Advent of Code 2016 Day 1."""


direction_to_move = {
    'N': (0, 1),
    'S': (0, -1),
    'W': (-1, 0),
    'E': (1, 0),
}

direction_to_angle = {
    'N': 0,
    'E': 90,
    'S': 180,
    'W': 270,
}

angle_to_direction = {
    0: 'N',
    90: 'E',
    180: 'S',
    270: 'W',
}

rotation_to_angle = {
    'R': 90,
    'L': -90,
}


def main(file_input='input.txt'):
    items = get_file_contents(file_input)[0].strip().split(', ')
    directions = parse_directions(items)
    final_position, visited_order = follow_directions(directions)
    distance_to_final = get_distance_to(final_position, (0, 0))
    print(f'Distance to final position: {distance_to_final}')
    first_visited_twice = find_first_visited_twice(visited_order)
    distance_to_visited_twice = get_distance_to(first_visited_twice, (0, 0))
    print(f'Distance to first visited twice: {distance_to_visited_twice}')


def get_distance_to(position, to_position):
    """Get distance from position to to_position."""
    return sum(abs(pos_coord - to_coord)
               for pos_coord, to_coord in zip(position, to_position))


def find_first_visited_twice(visited_order):
    """Find first position that repeats in visited_order."""
    visited = set()
    for location in visited_order:
        if location in visited:
            return location
        visited.add(location)
    return None


def follow_directions(directions):
    """Follow directions one-by-one.

    Returns final position and list with order in which
    locations were visited.
    """
    position = (0, 0)
    visited_order = []
    facing = 'N'
    for rotate, steps in directions:
        facing = rotation(facing, rotate)
        move = direction_to_move[facing]
        for _ in range(steps):
            position = move_position(position, move)
            visited_order.append(position)
    return position, visited_order


def move_position(old_position, move):
    """Move from old_position by move."""
    return tuple(
        position + change
        for position, change in zip(old_position, move)
    )


def rotation(facing, rotate_by):
    """Rotate facing by rotate_to.

    Returns new facing direction.
    """
    return angle_to_direction[
        (direction_to_angle[facing] + rotation_to_angle[rotate_by]) % 360
    ]


def parse_directions(items):
    """Parse items to directions."""
    return [parse_direction(direction)
            for direction in items]


def parse_direction(item):
    """Parse direction to tuple with rotation and number of steps."""
    return item[0], int(item[1:])


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
