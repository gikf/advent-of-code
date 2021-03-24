"""Advent of Code 2018 Day 12."""


PLANT = '#'
EMPTY = '.'


def main(file_input='input.txt'):
    initial, _, *lines = [
        line.strip() for line in get_file_contents(file_input)]
    rules = parse_rules(lines)
    after_20 = pots_sum_after_n_generations(parse_pots(initial), rules, 20)
    print(f'After 20 generations: {after_20}')
    after_50_billions = pots_sum_after_n_generations(
        parse_pots(initial), rules, 50_000_000_000)
    print(f'After fifty billion generations: {after_50_billions}')


def pots_sum_after_n_generations(pots, rules, n=20):
    """Calculate pot numbers sum after n generations."""
    pot_sums = [sum_numbers_of_pots_with_plant(pots)]
    for generation in range(n):
        pots = spread_generation(pots, rules)
        pot_sums.append(sum_numbers_of_pots_with_plant(pots))
        if generation > 2 and are_increments_the_same(pot_sums):
            generations_left = n - generation - 1
            increment = pot_sums[-1] - pot_sums[-2]
            return generations_left * increment + pot_sums[-1]
    return pot_sums[-1]


def are_increments_the_same(pot_sums):
    """Check if value increments between generations are the same."""
    return pot_sums[-2] - pot_sums[-3] == pot_sums[-1] - pot_sums[-2]


def spread_generation(pots, rules):
    """Follow pots by one generation."""
    prev_pots = '...' + ''.join(pot for pot, _ in pots) + '...'
    next_pots = '..'
    for index, pot in enumerate(prev_pots[2:-2], start=2):
        cur_pots = prev_pots[index - 2:index + 3]
        next_pots += rules.get(cur_pots, EMPTY)

    for func in (handle_front_pots, trim_last_pot):
        pots, next_pots = handle_front_pots(pots, next_pots)

    for index, next_pot in enumerate(next_pots):
        pots[index][0] = next_pot
    return pots


def trim_last_pot(pots, next_pots):
    """Handle last additional pot in pots."""
    if next_pots[-1] == PLANT:
        last_pot = pots[-1][1]
        pots = pots + [
            [next_pots[-1], last_pot + 1]]
        pots, next_pots
    return pots, next_pots[:-1]


def handle_front_pots(pots, next_pots):
    """Handle front, additional pots in pots."""
    if next_pots[2] == PLANT:
        first_pot = pots[0][1]
        pots = [
            [next_pots[2], first_pot - 1]] + pots
        return pots, next_pots[2:]
    return pots, next_pots[3:]


def sum_numbers_of_pots_with_plant(pots):
    """Sum numbers of all pots which contain plant."""
    return sum(
        index for pot, index in pots
        if pot == PLANT
    )


def parse_rules(lines):
    """Parse rules."""
    return dict(line.split(' => ') for line in lines)


def parse_pots(initial):
    """Parse initial pots."""
    return [[pot, index]
            for index, pot in enumerate(initial.split(': ')[1])]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
