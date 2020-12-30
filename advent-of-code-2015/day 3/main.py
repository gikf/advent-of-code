"""Advent of Code 2015 Day 3."""
from collections import defaultdict


moves = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, 1),
    'v': (0, -1),
}


def main(input_file='input.txt'):
    directions = get_file_contents(input_file)[0]
    visited_homes = direct_santa(directions)
    print(f'Homes with at least one present: {len(visited_homes)}')
    visited_homes_with_robo_santa = direct_santa(directions, santas_num=2)
    print('Homes with at least one present with Robo-Santa: '
          f'{len(visited_homes_with_robo_santa)}')


def direct_santa(directions, santas_num=1):
    """Direct santas_num of santas according to the directions.

    Santas start from the same point and then take directions in turns.
    """
    homes = defaultdict(int)
    santas = [[0, 0] for _ in range(santas_num)]
    for santa in santas:
        homes[tuple(santa)] += 1
    for move_number, direction in enumerate(directions):
        cur_santa = santas[move_number % santas_num]
        cur_move = moves[direction]
        for index, (position, change) in enumerate(zip(cur_santa, cur_move)):
            cur_santa[index] = position + change
        homes[tuple(cur_santa)] += 1
    return homes


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
