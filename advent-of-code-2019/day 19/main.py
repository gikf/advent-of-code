"""Advent of Code 2019 Day 19."""
from collections import defaultdict


TRACTORED = '#'
EMPTY = '.'
STATES = {
    0: EMPTY,
    1: TRACTORED,
}


def main(file_input='input.txt'):
    intcodes = [
        int(num)
        for num in get_file_contents(file_input)[0].strip().split(',')]
    grid = beam_grid(intcodes, 50, 50)
    tractored = count_on_grid(grid, TRACTORED)
    print('Number of points affected by tractor beam in the nearest 50x50 '
          f'area: {tractored}')
    row, col = find_square_in_beam(intcodes, 100)
    print('Value after multiplicating X coordinate by 10000 and adding Y:',
          col * 10000 + row)


def find_square_in_beam(program, square_size):
    """Find first occurrence of square with size square_size in the beam."""
    row = square_size + 1
    last_row_first = 0
    while True:
        col = last_row_first + 1
        while True:
            result = check_coordinates(program, row, col)
            if result == 1:
                last_row_first = col
                opposite_corner = check_coordinates(
                    program, row - square_size + 1, col + square_size - 1)
                if opposite_corner == 1:
                    return row - square_size + 1, col
                break
            col += 1
        row += 1


def beam_grid(program, rows, cols):
    """Check with program beam effect on the grid of size (rows, cols)."""
    grid = [[EMPTY for _ in range(cols)]
            for _ in range(rows)]
    last_row_first = 0
    for row_no, row in enumerate(grid):
        for col_no, _ in enumerate(row[last_row_first:], start=last_row_first):
            result = check_coordinates(program, row_no, col_no)
            passed_affected_points = (
                result == 0 and grid[row_no][col_no - 1] == TRACTORED)
            if passed_affected_points:
                break
            grid[row_no][col_no] = STATES[result]
            if col_no == 0:
                continue
            first_affected_point_in_row = (
                result == 1 and grid[row_no][col_no - 1] == EMPTY)
            if first_affected_point_in_row:
                last_row_first = col_no
    return grid


def check_coordinates(program, row, col):
    """Check (row, col) coordinates with program."""
    state = get_state()
    state['input'].extend([col, row])
    _, state = process_program(program[:], state)
    return state['output'][-1]


def count_on_grid(grid, wanted):
    """Count occurrences of wanted on the grid."""
    return sum(row.count(wanted) for row in grid)


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
