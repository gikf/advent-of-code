"""Advent of Code 2018 Day 15."""
from collections import deque
from copy import deepcopy
from functools import lru_cache


ELF = 'E'
EMPTY = '.'
GOBLIN = 'G'
WALL = '#'
MOVES = (
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0)
)
ENEMIES = {
    'E': 'G',
    'G': 'E',
}

example = '''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######'''.split('\n')

example = '''#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######'''.split('\n')

example = '''#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######'''.split('\n')

example = '''#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######'''.split('\n')

example = '''#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######'''.split('\n')

example = '''#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########'''.split('\n')


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    caves = parse_map(lines)
    last_round, final_caves = get_battle_outcome(deepcopy(caves))
    hit_points_left = sum_alive_units(final_caves)
    print(f'Outcome of the battle: {last_round * hit_points_left}')
    hit_points_left, final_round = lowest_win(caves)
    print('Outcome of the battle, with elves winning without loses: '
          f'{hit_points_left * final_round}')


def lowest_win(caves):
    attack = 3
    units = find_units(caves)
    while True:
        attack += 1
        elves_before = count_units(caves, units, ELF)
        cur_caves = deepcopy(caves)
        adjust_attack(cur_caves, units, ELF, attack)

        final_round, final_caves = get_battle_outcome(cur_caves, ELF)
        final_units = find_units(final_caves)

        elves_after = count_units(final_caves, final_units, ELF)
        if elves_before == elves_after:
            return sum_alive_units(final_caves), final_round


def count_units(caves, units, wanted_type):
    """Count number of units with wanted_type among units."""
    count = 0
    for row, col in units:
        unit_type, _, _ = get_cell(caves, row, col)
        if unit_type == wanted_type:
            count += 1
    return count


def adjust_attack(caves, units, adjust_unit, value):
    """Adjust attack of adjust_unit in units to value."""
    for row, col in units:
        unit = get_cell(caves, row, col)
        unit_type = unit[0]
        if unit_type == adjust_unit:
            unit[1] = value


def sum_alive_units(caves):
    """Sum hit points left of units in caves."""
    return sum(get_cell(caves, row, col)[2] for row, col in find_units(caves))


def get_battle_outcome(caves, protect=None):
    """Get battle outcome for caves."""
    cur_round = 0
    while one_round(caves, protect):
        cur_round += 1
    return cur_round, caves


def one_round(caves, protect=None):
    """Execute one round on caves.

    Return False if battle ended in this round, otherwise True."""
    units = find_units(caves)
    for cur_unit in sorted(units):
        cur_row, cur_col = cur_unit
        cur_cell = get_cell(caves, cur_row, cur_col)
        if cur_cell == EMPTY:
            continue

        enemies = find_enemy_units(caves, cur_unit, units)
        if not enemies:
            return False

        enemies_in_range = get_enemies_in_range(enemies, cur_row, cur_col)
        if not enemies_in_range:
            next_move = get_next_move(caves, enemies, cur_row, cur_col)
            if not next_move:
                continue
            units = move_unit(caves, units, cur_unit, next_move)
            enemies_in_range = get_enemies_in_range(enemies, *next_move)
        if not enemies_in_range:
            continue

        attack_target = get_attack_target(caves, enemies_in_range)
        killed = hit(caves, cur_unit, attack_target)
        if protect is not None and protect == killed:
            return False
    return True


def get_attack_target(caves, enemies_in_range):
    """Get attack target from enemies_in_range."""
    enemies_by_position = sorted(enemies_in_range)
    enemies_by_hit_points = sorted(
        enemies_by_position,
        key=lambda enemy: get_cell(caves, enemy[0], enemy[1])[2])
    return enemies_by_hit_points[0]


def get_enemies_in_range(enemies, row, col):
    """Get enemies in range from enemies."""
    return [enemy for enemy in enemies
            if enemy in get_adjacent(row, col)]


def hit(caves, attacker, target):
    """Hit target with attack."""
    target_row, target_col = target
    unit = get_cell(caves, target_row, target_col)
    _, attack, _ = get_cell(caves, *attacker)
    unit[2] -= attack
    if unit[2] <= 0:
        caves[target_row][target_col] = EMPTY
        return unit[0]
    return None


def move_unit(caves, units, position, next_position):
    """Move unit from position to next_position."""
    row, col = position
    next_row, next_col = next_position
    caves[row][col], caves[next_row][next_col] = (
        caves[next_row][next_col], caves[row][col])
    units.remove((row, col))
    units.add((next_row, next_col))
    return units


def get_next_move(caves, enemies, row, col):
    """Get next move, or return None if next move is not possible."""
    possible_targets = free_cells_in_range_of_targets(caves, enemies)
    if not possible_targets:
        return None

    distances = get_distances(caves, row, col)
    targets_with_distances = [
        (get_cell(distances, target_row, target_col), (target_row, target_col))
        for target_row, target_col in possible_targets]
    minimum_distance, _ = min(targets_with_distances)
    if minimum_distance == float('inf'):
        return None

    closest_targets = get_closest_targets(
        targets_with_distances, minimum_distance)
    adjacent_cells = get_steps_from_adjacent_cells(
        caves, closest_targets, row, col)
    if not adjacent_cells:
        return None
    return sorted(adjacent_cells)[0][1]


def get_closest_targets(targets_with_distances, min_distance):
    """Get closest targets with min_distance from targets_with_distances."""
    return [
        (target_row, target_col)
        for distance, (target_row, target_col) in targets_with_distances
        if distance == min_distance]


def get_steps_from_adjacent_cells(caves, closest_targets, row, col):
    """Get steps from adjacent cells to closest_targets."""
    adjacent_cells = []
    for target_row, target_col in closest_targets:
        target_distances = get_distances(caves, target_row, target_col)
        steps_to_target = [
            (get_cell(target_distances, cur_row, cur_col), (cur_row, cur_col))
            for cur_row, cur_col in get_free_adjacent(caves, row, col)]
        adjacent_cells.extend(steps_to_target)
    return adjacent_cells


def free_cells_in_range_of_targets(caves, targets):
    """Find free cells in range of targets."""
    cells_in_range = []
    for row_no, col_no in targets:
        cells_in_range.extend(get_free_adjacent(caves, row_no, col_no))
    return cells_in_range


def get_distances(caves, row, col):
    """Get distances in caves from (row, col).

    Uses BFS to search distances.
    """
    queue = deque()
    visited = set()
    queue.append((row, col))
    distances = [[float('inf') for _ in range(len(caves[0]))]
                 for _ in range(len(caves))]
    distances[row][col] = 0
    while queue:
        cur_row, cur_col = queue.popleft()
        cur_distance = get_cell(distances, cur_row, cur_col)
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        for next_row, next_col in get_free_adjacent(caves, cur_row, cur_col):
            next_cell = get_cell(caves, next_row, next_col)
            if (next_row, next_col) in visited or next_cell != EMPTY:
                continue
            distances[next_row][next_col] = cur_distance + 1
            queue.append((next_row, next_col))
    return distances


def get_free_adjacent(caves, row, col):
    """Get EMPTY adjacent cells to (row, col) in caves."""
    return [(cur_row, cur_col)
            for cur_row, cur_col in get_adjacent(row, col)
            if get_cell(caves, cur_row, cur_col) == EMPTY]


@lru_cache()
def get_adjacent(row, col):
    """Get adjacent cells to (row, col) in caves."""
    adjacent = []
    for row_change, col_change in MOVES:
        next_row = row + row_change
        next_col = col + col_change
        adjacent.append((next_row, next_col))
    return adjacent


def get_cell(caves, row, col):
    """Get (row, col) cell in caves."""
    return caves[row][col]


def find_units(caves):
    """Find units in caves."""
    units = set()
    for row_no, row in enumerate(caves):
        for col_no, col in enumerate(row):
            if col in (EMPTY, WALL):
                continue
            units.add((row_no, col_no))
    return units


def find_enemy_units(caves, unit, all_units):
    """Find enemy of unit in caves from all_units."""
    enemy = ENEMIES[get_cell(caves, *unit)[0]]
    enemies = set()
    for row, col in all_units:
        cell = get_cell(caves, row, col)
        if isinstance(cell, list) and cell[0] == enemy:
            enemies.add((row, col))
    return enemies


def parse_map(lines):
    """Parse lines to map, with units being list.

    Units list consist of unit type, attack and hit_points.
    """
    return [
        [col if col not in (ELF, GOBLIN) else [col, 3, 200]
         for col in row]
        for row in lines
    ]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
