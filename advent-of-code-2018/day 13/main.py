"""Advent of Code 2018 Day 13."""
from copy import deepcopy


CARTS = '<>^v'
INTERSECTION = '+'
CURVES = '\\/'
cart_to_direction = {
    '<': 180,
    '^': 90,
    '>': 0,
    'v': 270,
}
direction_to_move = {
    0: (0, 1),
    90: (-1, 0),
    180: (0, -1),
    270: (1, 0),
}
direction_to_cart = {
    0: '>',
    90: '^',
    180: '<',
    270: 'v',
}
turns = {
    0: 90,
    1: 0,
    2: -90,
}
next_direction = {
    0: {
        '\\': 270,
        '/': 90,
    },
    90: {
        '\\': 180,
        '/': 0,
    },
    180: {
        '\\': 90,
        '/': 270,
    },
    270: {
        '\\': 0,
        '/': 180,
    },
}


def main(file_input='input.txt'):
    lines = [[*line.strip('\n')] for line in get_file_contents(file_input)]
    carts = find_carts(lines)
    tracks = remove_carts(lines)
    collision = follow_tracks(tracks, deepcopy(carts))
    print('First collision:', ','.join(str(num) for num in collision[::-1]))
    last_cart_location = follow_tracks(tracks, deepcopy(carts), True)
    print('Last cart position after all crashes:',
          ','.join(str(num) for num in last_cart_location[::-1]))


def follow_tracks(tracks, carts, prevent_collision=False):
    """Follow tracks with carts. Optionally prevent ending with collision."""
    while len(carts) > 1:
        carts, collisions = move_carts(tracks, carts)
        if collisions and not prevent_collision:
            return collisions[0]
    return carts[0][0]


def find_repeated_position(carts):
    """Find position taken by two carts - colliding."""
    repeated = []
    seen_positions = set()
    for cur_position, *_ in carts:
        position = tuple(cur_position)
        if position in seen_positions:
            repeated.append(cur_position)
        seen_positions.add(position)
    return repeated


def move_carts(tracks, carts):
    """Move carts by one on tracks."""
    collisions = []
    for cart in sorted(carts):
        position, direction, turn = cart
        move = direction_to_move[direction]
        next_position = [pos + change for pos, change in zip(position, move)]

        next_square = get_square(tracks, next_position)
        if next_square == INTERSECTION:
            next_direction, next_turn = turn_cart(direction, turn)
            cart[1] = next_direction
            cart[2] = next_turn
        elif is_curve(next_square):
            next_direction = curve_cart(direction, next_square)
            cart[1] = next_direction
        cart[0] = next_position

        repeated_position = find_repeated_position(carts)
        if repeated_position:
            collisions.extend(repeated_position)
            carts = remove_collided_carts(carts, repeated_position)
    return carts, collisions


def remove_collided_carts(carts, repeated_position):
    """Remove carts colliding on the repeated_position."""
    return [cart for cart in carts
            if cart[0] not in repeated_position]


def curve_cart(direction, curve):
    """Move cart over the curve."""
    return next_direction[direction][curve]


def turn_cart(direction, turn):
    """Turn cart from direction, depending on the turn type."""
    return (direction + turns[turn]) % 360, (turn + 1) % len(turns)


def is_curve(square):
    """Check if square is one of the curves."""
    return square in CURVES


def get_square(tracks, position):
    """Get square from tracks with position."""
    row, col = position
    return tracks[row][col]


def remove_carts(lines):
    """Remove carts from lines, replacing them with normal tracks."""
    for row_no, row in enumerate(lines):
        for col_no, square in enumerate(row):
            if square in '<>':
                lines[row_no][col_no] = '-'
            elif square in 'v^':
                lines[row_no][col_no] = '|'
    return lines


def find_carts(lines):
    """Find carts in lines. Return list of lists with cart parameters."""
    carts = []
    for row_no, row in enumerate(lines):
        for col_no, square in enumerate(row):
            if square not in CARTS:
                continue
            carts.append([[row_no, col_no], cart_to_direction[square], 0])
    return carts


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
