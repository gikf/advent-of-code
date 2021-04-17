"""Advent of Code 2019 Day 11."""
from collections import defaultdict


BLACK = ' '
WHITE = '#'
COLOR_TO_INPUT = {
    BLACK: 0,
    WHITE: 1,
}
OUTPUT_TO_COLOR = {
    0: BLACK,
    1: WHITE,
}
TURNS = {
    0: 90,
    1: -90,
}
DIRECTIONS = {
    90: (-1, 0),
    180: (0, -1),
    270: (1, 0),
    0: (0, 1),
}


def main(file_input='input.txt'):
    intcodes = [
        int(num)
        for num in get_file_contents(file_input)[0].strip().split(',')]
    hull = paint_hull(intcodes[:])
    print(f'Panels painted at least once: {len(hull)}')
    hull = paint_hull(intcodes[:], WHITE)
    painted_hull = show_hull(hull)
    print('Registration identifier:')
    for row in painted_hull:
        print(''.join(row))


def paint_hull(program, first_panel=BLACK):
    """Paint hull starting from first_panel, and following program output."""
    hull = defaultdict(lambda: BLACK)
    direction = 90
    position = (0, 0)
    hull[position] = first_panel
    state = get_state()
    while 'finished' not in state:
        cur_color = hull[position]
        cur_input = COLOR_TO_INPUT[cur_color]
        state['input'].append(cur_input)

        program, state = process_program(program, state)
        turn, paint = [state['output'].pop() for _ in range(2)]
        hull[position] = OUTPUT_TO_COLOR[paint]
        direction = turn_robot(direction, turn)
        position = move_forward(direction, position)
    return hull


def show_hull(hull):
    """Show hull on the 2D grid."""
    yes, xes = list(zip(*hull))
    row_max, col_max = [max(values) for values in (yes, xes)]
    grid = [[BLACK for _ in range(col_max + 1)]
            for _ in range(row_max + 1)]
    for (row, col), panel in hull.items():
        grid[row][col] = panel
    return grid


def turn_robot(direction, turn):
    """Turn robot from the current direction."""
    return (direction + TURNS[turn]) % 360


def move_forward(direction, position):
    """Move position forward by one step in the correct direction."""
    row_change, col_change = DIRECTIONS[direction]
    row, col = position
    return row + row_change, col + col_change


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
        return True, 9999
    # print(state)
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
