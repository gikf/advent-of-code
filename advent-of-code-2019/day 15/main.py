"""Advent of Code 2019 Day 15."""
from copy import deepcopy
from collections import defaultdict, deque


def main(file_input='input.txt'):
    intcodes = [
        int(num)
        for num in get_file_contents(file_input)[0].strip().split(',')]
    locations, steps = explore_map(intcodes[:])
    print(f'Fewest steps to oxygen system: {steps}')
    grid = create_grid_from_locations(locations)
    minutes = spread_oxygen(grid)
    print(f'Minutes to fill map with oxygen: {minutes}')


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
MOVE_TO_COMMAND = {
    'n': NORTH,
    's': SOUTH,
    'w': WEST,
    'e': EAST,
}
COMMAND_TO_MOVE = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    WEST: (0, -1),
    EAST: (0, 1),
}
WALL = '#'
EMPTY = '.'
OXYGEN = 'O'
DROID = 'D'
START = 'X'
OUTPUT = {
    0: WALL,
    1: EMPTY,
    2: OXYGEN,
}


def explore_map(program):
    """Explore map in program with droid.

    Returns dictionary with locations - coordinates: location_type
    and number of steps to reach oxygen system.
    """
    locations = {(0, 0): START}
    visited_positions = set()
    queue = deque()
    queue.append(((0, 0), program, get_state(), 0))
    oxygen_steps = None
    while queue:
        position, program, state, moves_count = queue.popleft()
        if position in visited_positions:
            continue
        for input_move in MOVE_TO_COMMAND:
            cur_program, cur_state = [
                deepcopy(parameter) for parameter in (program, state)]
            move_command = MOVE_TO_COMMAND[input_move]
            cur_state['input'].append(move_command)
            cur_count = moves_count + 1

            cur_position = get_new_position(position, move_command)

            cur_program, cur_state = process_program(cur_program, cur_state)
            result = OUTPUT[cur_state['output'].pop()]

            locations[cur_position] = result
            if result == WALL:
                continue
            elif result == OXYGEN:
                oxygen_steps = cur_count
            queue.append((cur_position, cur_program, cur_state, cur_count))
        visited_positions.add(position)
    return locations, oxygen_steps


def get_new_position(position, move_command):
    """Get new position from position after move_command."""
    return tuple(
        [value + change
         for value, change in zip(position, COMMAND_TO_MOVE[move_command])])


def spread_oxygen(grid):
    """Spread oxygen in grid. Return minutes it takes to fill map."""
    oxygen_location = find_on_grid(grid, OXYGEN)
    queue = deque([(0, oxygen_location)])
    visited = set()
    last_minute = None
    while queue:
        minutes, position = queue.popleft()
        if position in visited:
            continue
        visited.add(position)
        for move in COMMAND_TO_MOVE.values():
            cur_row, cur_col = [
                value + change
                for value, change in zip(position, move)]
            if grid[cur_row][cur_col] == WALL:
                continue
            queue.append((minutes + 1, (cur_row, cur_col)))
        last_minute = minutes
    return last_minute


def find_on_grid(grid, wanted):
    """Find location of wanted on grid."""
    for row_no, row in enumerate(grid):
        for col_no, col in enumerate(row):
            if col == wanted:
                return (row_no, col_no)
    return None


def create_grid_from_locations(locations, droid_position=(0, 0)):
    """Create grid from locations, with droid at (0, 0) in locations."""
    yes, xes = zip(*locations)
    range_y, range_x = [(min(values), max(values)) for values in (yes, xes)]
    adjust_row, adjust_col = [abs(range_y[0]), abs(range_x[0])]
    grid = [[' ' for _ in range(range_x[1] + adjust_col + 1)]
            for _ in range(range_y[1] + adjust_row + 1)]
    for (row, col), status in locations.items():
        grid[row + adjust_row][col + adjust_col] = status
    droid_y, droid_x = [
        value + adjust
        for value, adjust in zip(droid_position, (adjust_row, adjust_col))]
    grid[droid_y][droid_x] = DROID
    return grid


def process_program(program, state):
    """Process program."""
    position = state['last_position'] if state['last_position'] else 0
    while position < len(program):
        state['last_position'] = position
        start = position
        instruction = program[start]
        modes, opcode = parse_instruction(instruction)
        if not opcode:
            break
        parameters, opfunc = get_operation(opcode)
        if opfunc is None:
            state['finished'] = True
            break

        end = start + parameters + 1
        func_parameters = program[start + 1:end]

        increment, result = opfunc(
            program, state, func_parameters, modes)
        if increment:
            position += result + 1
        else:
            position = result
    return program, state


def get_state(initial=None, input_value=None):
    """Get new state, filling initial and optional input_value."""
    return {
        'last_position': None,
        'initial': [initial] if initial is not None else [],
        'input': [input_value] if input_value is not None else [],
        'output': [],
        'relative': 0,
        'memory': defaultdict(int),
    }


def parse_instruction(instruction):
    """Parse instruction to modes and opcode."""
    opcode = instruction % 100
    result_modes = []
    modes = instruction // 100
    for _ in range(3):
        result_modes.append(modes % 10)
        modes = modes // 10
    return result_modes, opcode


def get_operation(opcode):
    """Opcode to operation function mapping."""
    opcodes = {
        1: (3, add_op),
        2: (3, mult_op),
        3: (1, input_op),
        4: (1, output_op),
        5: (2, jump_if_true),
        6: (2, jump_if_false),
        7: (3, less_than),
        8: (3, equals),
        9: (1, adjust_relative_base),
        99: (0, None),
    }
    return opcodes.get(opcode)


def write_value(program, state, target, value):
    """Write value to program or state memory."""
    try:
        program[target] = value
    except IndexError:
        state['memory'][target] = value


def add_op(program, state, parameters, modes):
    """Addition operation."""
    val1, val2, target = get_operation_values(
        program, state, parameters, modes)
    write_value(program, state, target, val1 + val2)
    return True, 3


def mult_op(program, state, parameters, modes):
    """Multiplication operation."""
    val1, val2, target = get_operation_values(
        program, state, parameters, modes)
    write_value(program, state, target, val1 * val2)
    return True, 3


def input_op(program, state, parameters, modes):
    """Input operation."""
    target = get_target_value(state, parameters[0], modes[0])
    if state['initial']:
        value = state['initial'].pop(0)
    elif state['input']:
        value = state['input'].pop(0)
    else:
        return False, 9999
    write_value(program, state, target, value)
    return True, 1


def output_op(program, state, parameters, modes):
    """Output operation."""
    value = get_param_values(program, state, parameters[:], modes[:])[0]
    state['output'].append(value)
    return True, 1


def jump_if_true(program, state, parameters, modes):
    """Jump if true operation."""
    val1, val2 = get_param_values(program, state, parameters, modes)
    if val1 != 0:
        return False, val2
    return True, 2


def jump_if_false(program, state, parameters, modes):
    """Jump if false operation."""
    val1, val2 = get_param_values(program, state, parameters, modes)
    if val1 == 0:
        return False, val2
    return True, 2


def less_than(program, state, parameters, modes):
    """Less than operation."""
    val1, val2, target = get_operation_values(
        program, state, parameters, modes)
    value = 1 if val1 < val2 else 0
    write_value(program, state, target, value)
    return True, 3


def equals(program, state, parameters, modes):
    """Equal operation."""
    val1, val2, target = get_operation_values(
         program, state, parameters, modes)
    value = 1 if val1 == val2 else 0
    write_value(program, state, target, value)
    return True, 3


def adjust_relative_base(program, state, parameters, modes):
    """Relative base adjusting action."""
    state['relative'] += get_param_values(
        program, state, parameters, modes)[0]
    return True, 1


def get_operation_values(program, state, parameters, modes):
    """Get operation values."""
    *params, target = parameters
    *value_modes, target_mode = modes
    val1, val2 = get_param_values(program, state, params, value_modes)
    target = get_target_value(state, target, target_mode)
    return val1, val2, target


def get_target_value(state, target, mode):
    """Get target value."""
    if mode == 2:
        return target + state['relative']
    return target


def get_param_values(program, state, parameters, modes):
    """Get values from program, based on parameters and modes."""
    vals = []
    for param, mode in zip(parameters, modes):
        if mode == 1:
            vals.append(param)
            continue
        elif mode == 2:
            param += state['relative']

        try:
            vals.append(program[param])
        except IndexError:
            vals.append(state['memory'][param])
    return vals


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()