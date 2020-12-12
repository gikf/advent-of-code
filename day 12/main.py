# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:34:34 2020
"""

MOVES = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
}

DIRECTIONS = {
    0: 'E',
    90: 'N',
    180: 'W',
    270: 'S',
}

DIRECTION_TO_DEG = {
    'E': 0,
    'N': 90,
    'W': 180,
    'S': 270,
}

RELATIVE_TURNS = {
    0: lambda x, y: (x, y),
    90: lambda x, y: (-y, x),
    180: lambda x, y: (-x, -y),
    270: lambda x, y: (y, -x)
}


def main():
    moves = [line.strip() for line in get_file_contents()]
    final_position = process_moves(moves)
    print(final_position)
    distance = get_manhattan_distance(*final_position)
    print(distance)
    final_waypoint_position = process_waypoint_moves(moves)
    print(final_waypoint_position)
    distance = get_manhattan_distance(*final_waypoint_position)
    print(distance)


def process_moves(moves):
    """Process moves.

    Actions:
        E - move east by given value
        N - move north by given value
        W - move west by given value
        S - move sount by given value
        L - rotate left by given angle
        R - rotate right by given angle
        F - move forward in the direction ship is facing by given value
    """
    x = y = 0
    direction = 'E'
    for move in moves:
        action, value = move[0], int(move[1:])
        if action in 'RL':
            cur_deg = DIRECTION_TO_DEG[direction]
            direction = DIRECTIONS[turn(
                cur_deg, value * (-1 if action == 'R' else 1)
            )]
        else:
            x_diff, y_diff = MOVES[action if action != 'F' else direction]
            x += x_diff * value
            y += y_diff * value
    return x, y


def process_waypoint_moves(moves):
    """Process moves according to the current waypoint coords - wx, wy.

    Actions:
        E - move waypoint east by given value
        N - move waypoint north by given value
        W - move waypoint west by given value
        S - move waypoint sount by given value
        L - rotate waypoint left by given angle
        R - rotate waypoint right by given angle
        F - move forward by the waypoint coords values by given number times
    """
    x = y = 0
    wx, wy = 10, 1
    for move in moves:
        action, value = move[0], int(move[1:])
        if action in 'RL':
            wx, wy = relative_turn(
                wx, wy, value * (-1 if action == 'R' else 1)
            )
        elif action == 'F':
            x += wx * value
            y += wy * value
        else:
            wx_diff, wy_diff = MOVES[action]
            wx += wx_diff * value
            wy += wy_diff * value
    return x, y


def get_manhattan_distance(x, y):
    """Calculate Manhattan distance of x, y to the 0, 0 point."""
    return abs(x) + abs(y)


def relative_turn(wx, wy, degs):
    """Turn wx and wy with degs angle by the 0, 0 point."""
    return RELATIVE_TURNS[degs % 360](wx, wy)


def turn(start, degs):
    """Turn start angle by degs."""
    return (start + degs) % 360


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
