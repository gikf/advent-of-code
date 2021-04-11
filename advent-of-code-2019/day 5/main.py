"""Advent of Code 2019 Day 5."""


def main(file_input='input.txt'):
    intcodes = [
        int(num)
        for num in get_file_contents(file_input)[0].strip().split(',')]
    runs = (1, 5)
    for input_value in runs:
        program = intcodes[:]
        state = {
            'input': [input_value],
            'output': [],
        }
        _, state = process_program(program, state)
        code = state['output'][-1]
        print(f'Diagnostic code after adding {input_value} as input: {code}')


def process_program(program, state):
    """Process program."""
    position = 0
    while True:
        start = position
        instruction = program[start]
        modes, opcode = parse_instruction(instruction)
        if not opcode:
            break
        parameters, opfunc = get_operation(opcode)
        if opfunc is None:
            break

        end = start + parameters + 1
        func_parameters = program[start + 1:end]

        increment, result = opfunc(program, state, func_parameters, modes)
        if increment:
            position += result + 1
        else:
            position = result
    return program, state


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
        99: (0, None),
    }
    return opcodes.get(opcode)


def add_op(program, _, parameters, modes):
    """Addition operation."""
    *params, target = parameters
    val1, val2 = get_operation_values(program, params, modes)
    program[target] = val1 + val2
    return True, 3


def mult_op(program, _, parameters, modes):
    """Multiplication operation."""
    *params, target = parameters
    val1, val2 = get_operation_values(program, params, modes)
    program[target] = val1 * val2
    return True, 3


def input_op(program, state, parameters, modes):
    """Input operation."""
    target = parameters[0]
    program[target] = state['input'][-1]
    return True, 1


def output_op(program, state, parameters, modes):
    """Output operation."""
    value = program[parameters[0]] if modes[0] == 0 else parameters[0]
    state['output'].append(value)
    return True, 1


def jump_if_true(program, _, parameters, modes):
    """Jump if true operation."""
    val1, val2 = get_operation_values(program, parameters, modes)
    if val1 != 0:
        return False, val2
    return True, 2


def jump_if_false(program, _, parameters, modes):
    """Jump if false operation."""
    val1, val2 = get_operation_values(program, parameters, modes)
    if val1 == 0:
        return False, val2
    return True, 2


def less_than(program, _, parameters, modes):
    """Less than operation."""
    *params, target = parameters
    val1, val2 = get_operation_values(program, params, modes)
    if val1 < val2:
        program[target] = 1
    else:
        program[target] = 0
    return True, 3


def equals(program, _, parameters, modes):
    """Equal operation."""
    *params, target = parameters
    val1, val2 = get_operation_values(program, params, modes)
    if val1 == val2:
        program[target] = 1
    else:
        program[target] = 0
    return True, 3


def get_operation_values(program, parameters, modes):
    """Get values from program, based on parameters and modes."""
    val1, val2 = [
        program[param] if mode == 0 else param
        for param, mode in zip(parameters, modes)
    ]
    return val1, val2


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
