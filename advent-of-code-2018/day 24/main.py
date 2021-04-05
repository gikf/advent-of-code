"""Advent of Code 2018 Day 24."""
import re


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    immune, infection = parse_units(lines)
    immune_end, infection_end = battle(immune, infection)
    print(f'Units left in the winning army: {count_units(infection_end)}')
    immune_end = battle_with_boost(*parse_units(lines))
    print('Units left in immune system for smallest boost resulting in immune '
          f'system win: {count_units(immune_end)}')


def battle_with_boost(immune, infection):
    """Battle immune units with infection units, boosting immune damage."""
    boost = 0
    initial_counts = get_value_of('count', (immune, infection))
    initial_damage = get_value_of('damage', (immune, infection))
    while True:
        boost += 1
        refill_units(initial_counts, 'count', immune, infection)
        refill_units(initial_damage, 'damage', immune, infection)
        boost_units(immune, boost)
        immune_end, infection_end = battle(immune, infection)
        if immune_end and not infection_end:
            return immune_end


def boost_units(units, value):
    """Boost units' damage with value."""
    for unit in units:
        units[unit]['damage'] += value


def battle(immune, infection):
    """Battle immune units with infection units."""
    while immune and infection:
        start_units = count_units(immune) + count_units(infection)
        immune, infection = fight(immune, infection)
        is_battle_finished = (
            count_units(immune) + count_units(infection) == start_units)
        if is_battle_finished:
            break
    return immune, infection


def fight(immune, infection):
    """Fight immune units against infection units."""
    immune_targets = select_targets(immune, infection)
    infection_targets = select_targets(infection, immune)
    all_unit_targets = {**immune_targets, **infection_targets}
    all_units = {**immune, **infection}
    units_by_initiative = sorted(
        all_units,
        key=lambda unit: all_units[unit]['initiative'],
        reverse=True
    )
    for attacker in units_by_initiative:
        if attacker not in all_unit_targets:
            continue
        target = all_unit_targets[attacker]
        is_target_killed = attack(all_units[attacker], all_units[target])
        if is_target_killed:
            del all_units[target]
            if target in all_unit_targets:
                del all_unit_targets[target]
    return separate_units_by_type(all_units)


def separate_units_by_type(all_units):
    """Separate all_units to their respective unit type group."""
    immune = {}
    infection = {}
    unit_type_to_group = {
        'immune': immune,
        'infection': infection,
    }
    for unit_no, unit in all_units.items():
        group = unit_type_to_group[unit['type']]
        group[unit_no] = unit
    return immune, infection


def attack(attacker, target):
    """Attack target with attacker.

    Return False if target is still alive, otherwise True.
    """
    damage = get_effective_damage(attacker, target)
    units_killed = damage // target['hit points']
    target['count'] -= units_killed
    if target['count'] <= 0:
        return True
    return False


def select_targets(attackers, defenders):
    """Select targets for attackers from defenders."""
    attacker_to_target = {}
    target_to_attacker = {}
    sortings = (
        lambda unit: attackers[unit]['initiative'],
        lambda unit: get_effective_power(attackers[unit]),
    )
    sorted_attackers = attackers
    for sorting_function in sortings:
        sorted_attackers = sorted(
            sorted_attackers, key=sorting_function, reverse=True)
    while sorted_attackers:
        attacker = sorted_attackers.pop(0)
        sortings = (
            lambda unit: defenders[unit]['initiative'],
            lambda unit: get_effective_power(defenders[unit]),
            lambda unit: get_effective_damage(
                attackers[attacker], defenders[unit]),
        )
        sorted_targets = defenders
        for sorting_function in sortings:
            sorted_targets = sorted(
                sorted_targets, key=sorting_function, reverse=True)
        if sorted_targets:
            cur_target = sorted_targets[0]
            if get_effective_damage(
                    attackers[attacker], defenders[cur_target]):
                attacker_to_target[attacker] = cur_target
                target_to_attacker[cur_target] = attacker
                defenders = {
                    unit_no: defender
                    for unit_no, defender in defenders.items()
                    if unit_no != cur_target}
    return attacker_to_target


def refill_units(unit_values, refill, immune, infection):
    """Refill units in immune and infection using unit_values."""
    type_to_group = {
        'immune': immune,
        'infection': infection
    }
    for unit_no, (count, unit_type) in unit_values.items():
        group_type = type_to_group[unit_type]
        group_type[unit_no][refill] = count


def get_value_of(value, unit_groups):
    """Get value from individual units in unit groups."""
    values = {}
    for group in unit_groups:
        for unit_no, unit in group.items():
            values[unit_no] = (unit[value], unit['type'])
    return values


def get_effective_damage(attacker, target):
    """Get effective damage of attacker against target."""
    if attacker['damage_type'] in target['immune']:
        return 0
    damage = get_effective_power(attacker)
    if attacker['damage_type'] in target['weak']:
        damage *= 2
    return damage


def get_effective_power(unit):
    """Get effective power of unit."""
    return unit['count'] * unit['damage']


def count_units(units):
    """Count total number of units."""
    return sum(unit['count'] for _, unit in units.items())


def parse_units(lines):
    """Parse lines to immune and infection units."""
    immune = {}
    infection = {}
    cur_units = immune
    unit_type = 'immune'
    for unit_no, line in enumerate(lines[1:]):
        if not line:
            continue
        if line == 'Infection:':
            cur_units = infection
            unit_type = 'infection'
            continue
        unit = parse_unit(line, unit_type)
        cur_units[unit_no] = unit
    return immune, infection


def parse_unit(line, unit_type):
    """Parse line to unit representation with unit_type."""
    regex = r'''(\d+)             # number of units
                [\w\s]+?
                (\d+)             # hit points
                [\w\s]+?
                (\([\w;,\s]+\))?  # immunity and weaknesses
                [\w\s]+?
                (\d+\s\w+)   # damage with type
                [\w\s]+?
                (\d+)             # initiative'''
    count, hit_points, immunes, damage, initiative = re.findall(
        regex, line, re.VERBOSE)[0]
    damage, damage_type = [
        int(part) if part.isdigit() else part for part in damage.split()]
    count, hit_points, initiative = [
        int(num) for num in (count, hit_points, initiative)]
    immune = set()
    weak = set()
    if immunes:
        immunes = immunes[1:-1].split('; ')
        for attributes in immunes:
            to_type, attributes = attributes.split(' to ')
            if to_type == 'immune':
                immune = set(attributes.split(', '))
            else:
                weak = set(attributes.split(', '))
    return {
        'type': unit_type,
        'count': count,
        'hit points': hit_points,
        'immune': immune,
        'weak': weak,
        'damage': damage,
        'damage_type': damage_type,
        'initiative': initiative
    }


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
