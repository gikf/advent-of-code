"""Advent of Code 2016 Day 11."""
from collections import deque, namedtuple
import re


floor_data = namedtuple('floor', 'generator microchip')

example = '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''.split('\n')


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    floors = get_floors(4)
    setup_floors(floors, example)
    elevator = 0
    print(floors)
    steps = move_elements_to(floors, elevator, 3, set())
    print(steps)
    floors = get_floors(4)
    setup_floors(floors, lines)
    elevator = 0
    print(floors)
    steps = move_elements_to(floors, elevator, 3, set())
    print(steps)
    floors = get_floors(4)
    setup_floors(floors, lines)
    elevator = 0
    for shielding in ('elerium', 'dilithium'):
        floors[0].generator.add(shielding)
        floors[0].microchip.add(shielding)
    print(floors)
    steps = move_elements_to(floors, elevator, 3, set())
    print(steps)


def move_elements_to(floors, elevator, target_floor, memo):
    queue = deque([(floors, elevator, 0)])
    while queue:
        cur_floors, cur_elevator, cur_steps = queue.popleft()
        set_key = get_set_key(cur_elevator, cur_floors)
        if set_key in memo:
            continue
        memo.add(set_key)
        if are_lower_floors_empty(cur_floors, target_floor):
            return cur_steps
        next_moves = get_moves_from_floor(cur_floors, cur_elevator)
        for direction in get_elevator_directions(cur_floors, cur_elevator):
            was_valid = False
            next_moves = sorted(next_moves, key=len,
                                reverse=True if direction == 'up' else False)
            for move in next_moves:
                if can_short(direction, len(move), was_valid):
                    break
                next_floors, next_elevator = move_elements(
                    cur_floors, cur_elevator, move, direction)
                if not is_state_allowed(next_floors):
                    continue
                was_valid = True
                queue.append((next_floors, next_elevator, cur_steps + 1))
    return None


def can_short(direction, length, valid):
    """Check if rest of moves can be skipped."""
    return (valid
            and ((direction == 'up' and length == 1)
                 or (direction == 'down' and length == 2)))


def get_set_key(elevator, floors):
    """Get set key for elevator and floors state.

    Optimized per idea in https://www.reddit.com/r/adventofcode/comments/5hoia9/2016_day_11_solutions/db1v1ws/  # noqa
    Specific shielding name is disregarded, what matters is only
    how shielding pairs, numbered in appearing order, are positioned
    on the floors.
    """
    shielding_to_number = get_shielding_to_number(floors)
    return (elevator,
            tuple([tuple([shielding_to_number[generator]
                          for generator in floor.generator])
                   for floor in floors]),
            tuple([tuple([shielding_to_number[microchip]
                          for microchip in floor.microchip])
                   for floor in floors]))


def get_shielding_to_number(floors):
    """Get dict of shielding to number order in which they appear."""
    shielding_to_number = {}
    cur_number = 0
    for floor in floors:
        for part in (floor.generator, floor.microchip):
            for element in part:
                if element not in shielding_to_number:
                    shielding_to_number[element] = cur_number
                    cur_number += 1
    return shielding_to_number


def move_elements(floors, elevator, elements, direction):
    """Move elements on floors in elevator directions."""
    next_floors = floors[:]
    move = create_move(elements)
    cur_floor = next_floors[elevator]
    next_elevator = move_elevator(elevator, direction)
    next_floor = next_floors[next_elevator]
    next_floor = floor_data(
        tuple(set(next_floor.generator) | set(move.generator)),
        tuple(set(next_floor.microchip) | set(move.microchip)))
    cur_floor = floor_data(
        tuple(set(cur_floor.generator) - set(move.generator)),
        tuple(set(cur_floor.microchip) - set(move.microchip)))
    next_floors[elevator] = cur_floor
    next_floors[next_elevator] = next_floor
    return next_floors, next_elevator


def get_elevator_directions(floors, elevator):
    """Get possible directions for elevator and floors."""
    directions = []
    if len(floors) > elevator + 1:
        directions.append('up')
    if elevator > 0 and not are_lower_floors_empty(floors, elevator):
        directions.append('down')
    return directions


def move_elevator(elevator, direction):
    """Move elevator according to direction."""
    directions = {'up': 1, 'down': -1}
    return elevator + directions[direction]


def get_moves_from_floor(floors, floor_number):
    """Get moves from floor floor_number."""
    floor = floors[floor_number]
    floor = ({(shielding, 'generator') for shielding in floor.generator}
             | {(shielding, 'microchip') for shielding in floor.microchip})
    return get_moves(floor, set(), 2)


def get_moves(left, cur_move, limit):
    """Get possible moves from left of possible length limit."""
    if len(cur_move) == limit or not left:
        return {tuple(sorted(cur_move))}
    moves = set()
    if len(cur_move) > 0:
        moves = moves | {tuple(sorted(cur_move))}
    for element in left:
        next_moves = get_moves(
            left - {element},
            cur_move | {element},
            limit
        )
        moves = moves | next_moves
    return moves


def create_move(elements):
    """Create move from elements."""
    move = {'generator': set(),
            'microchip': set()}
    for shielding, element_type in elements:
        move[element_type].add(shielding)
    return floor_data(**move)


def setup_floors(floors, lines):
    """Set up floors according to lines."""
    for index, (_, line) in enumerate(zip(floors, lines)):
        elements = parse_floor(line)
        floor = {'generator': set(),
                 'microchip': set()}
        for shielding, element_type in elements:
            floor[element_type].add(shielding)
        floors[index] = floor_data(**floor)


def are_lower_floors_empty(floors, floor_number):
    """Check if floors lower than floor_number are empty."""
    return all(not floor.generator and not floor.microchip
               for index, floor in enumerate(floors[:floor_number]))


def is_state_allowed(floors):
    """Check if floors state is allowed."""
    return all(is_floor_valid(
        floor.generator, floor.microchip) for floor in floors)


def is_floor_valid(generators, microchips):
    """Check if floor is valid."""
    return (are_all_chips_connected(generators, microchips)
            or not generators)


def are_all_chips_connected(generators, microchips):
    """Check if all chips are connected to generator."""
    return all(chip in generators for chip in microchips)


def parse_floor(line):
    """Parse chips and generators on floor from line."""
    regex = r' a ([a-z]+)(?:-compatible)? ([a-z]+)'
    return re.findall(regex, line)


def get_floors(number):
    """Prepare number of floors."""
    return [floor_data((), ()) for _ in range(number)]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
