"""Advent of Code 2018 Day 9."""


def main(file_input='input.txt'):
    numbers = [int(part)
               for part in get_file_contents(file_input)[0].strip().split()
               if part.isdigit()]
    players_count, max_points = numbers
    players = [0 for _ in range(players_count)]
    for multiplier in (1, 100):
        result_players = play_marbles(
            players[:], get_starting_marble(), max_points * multiplier)
        print('Score of the winning Elf with last marble worth '
              f'{max_points * multiplier}: {max(result_players)}')


def play_marbles(players, start_marble, limit_points):
    """Play marbles with number of players and limit_points."""
    cur_marble = start_marble
    cur_points = 1
    cur_player = 0
    while cur_points <= limit_points:
        if cur_points % 23 == 0:
            for _ in range(7):
                cur_marble = cur_marble['prev']
            next_marble = get_marble(cur_points)
            players[cur_player] += next_marble['value']
            players[cur_player] += cur_marble['value']
            cur_marble = remove_marble(cur_marble)
        else:
            cur_marble = insert_marble(cur_points, cur_marble['next'])
        cur_points += 1
        cur_player = (cur_player + 1) % len(players)
    return players


def remove_marble(marble):
    """Remove marble."""
    marble['prev']['next'] = marble['next']
    marble['next']['prev'] = marble['prev']
    return marble['next']


def insert_marble(cur_points, cur_marble):
    """Insert marble with cur_points after cur_marble."""
    next_marble = get_marble(
        cur_points, cur_marble, cur_marble['next'])
    next_marble['prev']['next'] = next_marble
    next_marble['next']['prev'] = next_marble
    return next_marble


def get_starting_marble():
    """Get starting marble - with value 0 and pointing to itself."""
    starting_marble = get_marble()
    starting_marble['next'] = starting_marble
    starting_marble['prev'] = starting_marble
    return starting_marble


def get_marble(value=0, prev=None, next=None):
    """Get new marble, with value, prev and next."""
    return {'value': value, 'prev': prev, 'next': next}


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
