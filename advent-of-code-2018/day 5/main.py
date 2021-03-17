"""Advent of Code 2018 Day 5."""
import re


def main(file_input='input.txt'):
    polymer = get_file_contents(file_input)[0].strip()
    reacted_polymer = react_polymer(polymer)
    print(len(reacted_polymer))
    polymer_length, _ = find_shortest_polymer(polymer)
    print(polymer_length)


def find_shortest_polymer(polymer):
    """Find shortest polymer after removing one unit type from polymer."""
    reacted = []
    start = ord('a')
    end = ord('z')
    for unit_code in range(start, end + 1):
        unit = chr(unit_code)
        cur_polymer = remove_from_polymer(polymer, unit)
        reacted_polymer = react_polymer(cur_polymer)
        reacted.append((len(reacted_polymer), reacted_polymer))
    return min(reacted)


def remove_from_polymer(polymer, unit):
    """Remove all occurrences of unit, regardless of polarity from polymer."""
    regex = f'{unit}'
    return re.sub(regex, '', polymer, flags=re.IGNORECASE)


def react_polymer(polymer):
    """React polymer removing all units paired with opposite polarity."""
    next_polymer = []
    for cur_unit in polymer:
        prev_unit = next_polymer[-1] if next_polymer else ''
        if (prev_unit
                and cur_unit.lower() == prev_unit.lower()
                and cur_unit != prev_unit):
            next_polymer.pop()
            continue
        next_polymer.append(cur_unit)
    return ''.join(next_polymer)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
