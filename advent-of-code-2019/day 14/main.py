"""Advent of Code 2019 Day 14."""
from collections import defaultdict
import math


TRILLION = 1_000_000_000_000


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    reactions = parse_reactions(lines)
    order = order_reactions(reactions, 'FUEL')
    ore = find_required_ore(reactions, order, 'FUEL', 1)
    print(f'Minimum ORE to produce 1 FUEL: {ore}')
    fuel = produce_with_ore(reactions, order, ore, TRILLION)
    print(f'Maximum FUEL produced with one trillion ORE: {fuel}')


def produce_with_ore(reactions, order, one_fuel_ore, ore_for_fuel):
    """Find how much fuel can be produced with ore_for_fuel."""
    fuel = ore_for_fuel // one_fuel_ore
    while find_required_ore(reactions, order, 'FUEL', fuel) < ore_for_fuel:
        fuel += 1000
    fuel -= 1
    while find_required_ore(reactions, order, 'FUEL', fuel) > ore_for_fuel:
        fuel -= 1
    return fuel


def order_reactions(reactions, chemical):
    """Sort reactions starting from chemical."""
    seen = set()
    order = ['ORE'] + dfs(reactions, chemical, seen)
    return {chemical: index for index, chemical in enumerate(reversed(order))}


def dfs(reactions, chemical, seen):
    """DFS to traverse all reaction requirements for chemical."""
    seen.add(chemical)
    if chemical == 'ORE':
        return []
    order = []
    _, needed_chemicals = reactions[chemical]
    for next_chemical, _ in needed_chemicals.items():
        if next_chemical not in seen:
            order.extend(dfs(reactions, next_chemical, seen))
    return order + [chemical]


def find_required_ore(reactions, order, wanted, amount):
    """Find required ore to produce amount of wanted chemical."""
    ore = 0
    still_needed = defaultdict(int)
    still_needed[wanted] = amount
    while still_needed:
        needed_chemical = sorted(still_needed, key=order.get)[0]
        required = still_needed.pop(needed_chemical)
        produced_amount, chemicals = reactions[needed_chemical]
        needed_units = math.ceil(required / produced_amount)
        for chemical, chemical_amount in chemicals.items():
            if chemical == 'ORE':
                ore += needed_units * chemical_amount
            else:
                still_needed[chemical] += needed_units * chemical_amount
    return ore


def parse_reactions(lines):
    """Parse lines to reactions dictionary."""
    reactions = {}
    for line in lines:
        product, amount, requirements = parse_reaction(line)
        reactions[product] = (amount, requirements)
    return reactions


def parse_reaction(line):
    """Parse line to tuple of product, amount of product and requirements."""
    required, producing = line.split(' => ')
    amount, product = [int(part) if part.isdigit() else part
                       for part in producing.split()]
    requirements = {}
    for requirement in required.split(', '):
        needed, chemical = [int(part) if part.isdigit() else part
                            for part in requirement.split()]
        requirements[chemical] = needed
    return product, amount, requirements


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
