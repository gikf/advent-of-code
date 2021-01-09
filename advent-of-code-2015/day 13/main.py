"""Advent of Code 2015 Day 13."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    names, preferences = parse_preferences(lines)
    seatings = find_seatings(names, [])
    seatings_with_yourself = insert_name_to_seatings('yourself', seatings)
    scored_seatings = score_seatings(seatings, preferences)
    highest_happiness = sorted(scored_seatings, reverse=True)[0][0]
    print(f'Highest happines: {highest_happiness}')
    scored_seatings_with = score_seatings(seatings_with_yourself, preferences)
    highest_happiness_with_yourself = sorted(
        scored_seatings_with, reverse=True)[0][0]
    print('Highest happiness with added yourself: '
          f'{highest_happiness_with_yourself}')


def score_seating(seating, preferences):
    """Score seating using preferences."""
    score = 0
    table_size = len(seating)
    for index, name in enumerate(seating):
        for seat_index in ((index - 1) % table_size,
                           (index + 1) % table_size):
            seating_by = seating[seat_index]
            score += preferences.get(name, {}).get(seating_by, 0)
    return score


def score_seatings(seatings, preferences):
    """Score all seatings using preferences."""
    return [
        (score_seating(seating, preferences), seating)
        for seating in seatings
    ]


def insert_name_to_seatings(name, seatings):
    """Insert name to seatings in all possible places."""
    new_seatings = []
    for seating in seatings:
        for index, _ in enumerate(seating):
            new_seatings.append(seating[:index] + [name] + seating[index:])
        new_seatings.append(seating + [name])
    return new_seatings


def find_seatings(names, table):
    """Find all seating combinations for names."""
    if not names:
        return [table]
    seatings = []
    for name in names:
        cur_names = names - {name}
        seatings.extend(find_seatings(cur_names,
                                      table + [name]))
    return seatings


def parse_preferences(lines):
    """Parse preference lines to dictionary of dictionaries.

    dict -> dict -> int
    name -> neighbour -> score for name being seated by neighbour.
    """
    preferences = defaultdict(dict)
    for line in lines:
        name, *rest, neighbour = line[:-1].split()
        score = int(rest[2])
        preferences[name][neighbour] = score if rest[1] == 'gain' else -score
    return {*preferences.keys()}, preferences


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
