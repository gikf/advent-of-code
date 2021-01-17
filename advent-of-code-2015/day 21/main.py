"""Advent of Code 2015 Day 21."""


PLAYER = object()
BOSS = object()


weapons = ('Weapons', '''Dagger:        8     4       0
Shortsword:   10     5       0
Warhammer:    25     6       0
Longsword:    40     7       0
Greataxe:     74     8       0'''.split('\n'))

armor = ('Armor', '''Leather:      13     0      1
Chainmail:    31     0       2
Splintmail:   53     0       3
Bandedmail:   75     0       4
Platemail:   102     0       5'''.split('\n'))

rings = ('Rings', '''Damage +1:    25     1     0
Damage +2:    50     2       0
Damage +3:   100     3       0
Defense +1:   20     0       1
Defense +2:   40     0       2
Defense +3:   80     0       3'''.split('\n'))


def main(file_input='input.txt'):
    boss = parse_boss([line.strip() for line in get_file_contents(file_input)])
    possible_equipments = generate_equipment(
        parse_shops(weapons, armor, rings))
    equipment_cost = get_equipments_cost(possible_equipments)
    equipment_by_cost = sorted(equipment_cost)
    least_gold_to_spend = find_gold_for_winner(
        equipments=equipment_by_cost, boss=boss, wanted_winner=PLAYER)
    print('Least amount of gold to spend and win fight: '
          f'{least_gold_to_spend}')
    most_gold_to_lose = find_gold_for_winner(
        equipments=equipment_by_cost[::-1], boss=boss, wanted_winner=BOSS)
    print('Most amount of gold to spend and lose fight: '
          f'{most_gold_to_lose}')


def find_gold_for_winner(equipments,
                         boss,
                         wanted_winner,
                         player_hit_points=100):
    """Find how much gold will cost equipment for wanted_winner to  win.

    Equipments need to be ordered by the equipment cost.
    """
    for equipment_cost, items in equipments:
        player = get_player(items, player_hit_points)
        if fight(player, boss.copy()) is wanted_winner:
            return equipment_cost
    return -1


def fight(player, boss):
    """Simulate fight until one of sides get hit points 0 or lower."""
    winners = [PLAYER, BOSS]
    players = [player, boss]
    damages = [get_damage(attacker, defender)
               for attacker, defender in (players, players[::-1])]
    while True:
        for index, (attacker, defender) in enumerate((players, players[::-1])):
            defender['Hit Points'] -= damages[index]
            if defender['Hit Points'] <= 0:
                return winners[index]


def get_damage(attacker, defender):
    """Get damage dealt by attacker to defender."""
    damage = attacker['Damage'] - defender['Armor']
    return damage if damage > 0 else 1


def get_player(equipment, hit_points):
    """Get player based on equipment and hit_points."""
    values = {'Damage': 0, 'Armor': 0}
    for _, attributes in equipment:
        for attribute in ('Damage', 'Armor'):
            values[attribute] += attributes[attribute]
    return {'Hit Points': hit_points,
            'Damage': values['Damage'],
            'Armor': values['Armor']}


def get_equipments_cost(possible_equipments):
    """Get cost of each equipment in possible_equipments."""
    return [(calculate_equipment_cost(equipment), equipment)
            for equipment in possible_equipments]


def calculate_equipment_cost(equipment):
    """Calculate cost of equipment."""
    cost = 0
    for item in equipment:
        item_name, attributes = item
        cost += attributes['Cost']
    return cost


def generate_equipment(shops):
    """Generate equipment combinations."""
    categories = (('Weapons', 1, 1), ('Armor', 0, 1), ('Rings', 0, 2))
    equipment_categories = [
        generate_combinations(shops[items], count_min, count_max, [])
        for (items, count_min, count_max) in categories]
    return pick_equipment(equipment_categories, [])


def pick_equipment(categories, cur_pick):
    """Pick one item from each of categories."""
    if not categories:
        return [cur_pick]
    items = categories[0]
    picks = []
    for item in items:
        next_picks = pick_equipment(categories[1:], cur_pick + item)
        picks.extend(next_picks)
    return picks


def generate_combinations(items, count_min, count_max, cur_items):
    """Generate possible combinations of items froum count_min to count_max."""
    if len(cur_items) == count_max:
        return [cur_items]
    combinations = []
    if len(cur_items) >= count_min:
        combinations.append(cur_items)
    for item in items.items():
        item_name, _ = item
        next_items = items.copy()
        next_items.pop(item_name)
        next_combinations = generate_combinations(
            next_items,
            count_min,
            count_max,
            cur_items + [item]
        )
        combinations.extend(next_combinations)
    return combinations


def parse_shops(*shops):
    """Parse shops."""
    return {name: parse_shop(shop)
            for name, shop in shops}


def parse_shop(shop_lines):
    """Parse shop data to dictionary."""
    items = {}
    for line in shop_lines:
        name, values = line.split(':')
        cost, damage, armor = [int(value) for value in values.split()]
        items[name] = {'Cost': cost, 'Damage': damage, 'Armor': armor}
    return items


def parse_boss(lines):
    """Parse boss data from lines to dictionary."""
    boss = {}
    for line in lines:
        attribute, value = line.split(':')
        boss[attribute] = int(value)
    return boss


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
