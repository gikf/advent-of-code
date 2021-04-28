"""Advent of Code 2019 Day 22."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    deck = [number for number in range(10_007)]
    shuffles = parse_shuffles(lines)
    position_after_shuffles = follow_card(2019, len(deck), shuffles)
    print('Position of 2019 in 10007 card deck after shuffling:',
          f'{position_after_shuffles}')
    deck_size = 119_315_717_514_047
    position = 2020
    number_of_shuffles = 101_741_582_076_661


def follow_card(card, deck_size, shuffles):
    """Follow position of the card in deck of deck_size during shuffles."""
    position = card
    for shuffle, parameter in shuffles:
        shuffling = get_shuffle_follow(shuffle)
        position = shuffling(deck_size, position, parameter)
    return position


def get_shuffle_follow(shuffle):
    """Shuffle type to shuffle function mapping."""
    return {
        'cut': cut_follow,
        'new stack': stack_follow,
        'increment': increment_follow,
    }[shuffle]


def egcd(a, b):
    """Extended Euclidean algorithm for gcd."""
    if a == 0:
        return b, 0, 1
    gcd, y, x = egcd(b % a, a)
    return gcd, x - (b // a) * y, y


def mod_inverse(a, m):
    gcd, x, y = egcd(a, m)
    if gcd == 1:
        return x % m


def increment_follow(deck_size, position, increment):
    """Get new position after incrementing by increment."""
    return (position * increment) % deck_size


def cut_follow(deck_size, position, cut_value):
    """Get new position after cutting deck at cut_value."""
    return (position - cut_value) % deck_size


def stack_follow(deck_size, position, *_):
    """Get new position after stacking deck."""
    return deck_size - position - 1


def parse_shuffle(line):
    """Parse line to tuple with shuffle type and parameter."""
    if line.startswith('cut'):
        return 'cut', int(line[3:])
    elif line.startswith('deal into'):
        return 'new stack', None
    elif line.startswith('deal with'):
        offset = len('deal with increment')
        return 'increment', int(line[offset:])


def parse_shuffles(lines):
    """Parse shuffles from lines."""
    return [parse_shuffle(line) for line in lines]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
