"""Advent of Code 2019 Day 22."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    deck = [number for number in range(10_007)]
    shuffles = parse_shuffles(lines)
    position_after_shuffles = follow_card(
        2019, len(deck), shuffles, get_shuffle_follow)
    print('Position of 2019 in 10007 card deck after shuffling:',
          f'{position_after_shuffles}')
    deck_size = 119_315_717_514_047
    card = 2020
    number_of_shuffles = 101_741_582_076_661
    position = find_position_after_number_of_shuffles(
        shuffles, deck_size, card, number_of_shuffles)
    print(f'Position of card {card} in deck with {deck_size} cards '
          f'after {number_of_shuffles} shuffles: {position}')


def find_position_after_number_of_shuffles(
        shuffles, deck_size, card, number_of_shuffles):
    """Find position of card in deck_size after number_of_shuffles."""
    # Based on reddit
    initial_cards = [1, 0]
    a, b = follow_card(initial_cards, deck_size, shuffles, get_part2_shuffles)
    A = a_n = pow(a, number_of_shuffles, deck_size)
    B = b * (a_n - 1) * mod_inverse(a - 1, deck_size)
    position = (card - B) * mod_inverse(A, deck_size) % deck_size
    return position


def follow_card(card, deck_size, shuffles, shuffler):
    """Follow position of the card in deck of deck_size during shuffles."""
    position = card
    for shuffle, parameter in shuffles:
        shuffling = shuffler(shuffle)
        position = shuffling(deck_size, position, parameter)
    return position


def get_part2_shuffles(shuffle):
    """Shuffling functions for part 2."""
    return {
        'cut': cut_deck,
        'new stack': stack_deck,
        'increment': increment_deck
    }[shuffle]


def stack_deck(deck_size, cards, *_):
    """Make new stack from deck."""
    return [(-card + change) % deck_size
            for card, change in zip(cards, (0, -1))]


def cut_deck(deck_size, cards, cut):
    """Cut deck operation."""
    return [(card + change) % deck_size
            for card, change in zip(cards, (0, -cut))]


def increment_deck(deck_size, cards, increment):
    """Increment operation."""
    return [(card * increment) % deck_size for card in cards]


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
    """Modular inverse."""
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
