"""Advent of Code 2019 Day 7."""


def main(file_input='input.txt'):
    intcodes = [
        int(num)
        for num in get_file_contents(file_input)[0].strip().split(',')]
    highest_signal = find_highest_signal(intcodes[:], {0, 1, 2, 3, 4}, signal)
    print(f'Highest signal: {highest_signal}')
    highest_signal_with_feedback = find_highest_signal(
        intcodes[:], {9, 8, 7, 6, 5}, with_feedback_loop)
    print(f'Highest signal with feedback loop: {highest_signal_with_feedback}')


def find_highest_signal(intcodes, phase_set, signal_func):
    """Find highest signal from program, using signal_func and phase_set."""
    combinations = get_combinations(phase_set, [])
    highest_signal = float('-inf')
    for combination in combinations:
        state = {
            'input': combination,
            'output': [0],
        }
        output_signal = signal_func(state, intcodes, combination)
        highest_signal = max(highest_signal, output_signal)
    return highest_signal


def with_feedback_loop(state, intcodes, combination):
    """Find signal send from program after using feedback loop."""
    programs = []
    for _ in range(5):
        state = get_state(combination.pop(0))
        programs.append((intcodes[:], state))
    programs[0][1]['initial'].append(0)
    connect_amplifers(programs)
    while all('finished' not in program[1] for program in programs):
        for program, state in programs:
            if 'finished' in state:
                continue
            program, state = process_program(program, state)
    return programs[4][1]['output'][0]


def signal(state, intcodes, combination):
    """Find signal send from program after processing intcodes on state."""
    for initial in combination:
        state = get_state(initial, state['output'][0])
        final_program, state = process_program(intcodes[:], state)
    return state['output'][0]


def connect_amplifers(programs):
    """Connect amplifiers by connecting output to the input of next one."""
    for program_no, (_, state) in enumerate(programs[1:]):
        state['input'] = programs[program_no][1]['output']
    programs[4][1]['output'] = programs[0][1]['input']


def get_state(initial, input_value=None):
    """Get new state, filling initial and optional input_value."""
    return {
        'last_position': None,
        'initial': [initial],
        'input': [input_value] if input_value is not None else [],
        'output': [],
    }


def get_combinations(numbers_left, cur_combination):
    """Get combinations from numbers_left."""
    if not numbers_left:
        return [cur_combination]
    combinations = []
    for number in numbers_left:
        combinations.extend(get_combinations(
            numbers_left - {number},
            cur_combination + [number]
        ))
    return combinations


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
    # print('input:', state['input'], 'initial:', state['initial'])
    if state['initial']:
        program[target] = state['initial'].pop(0)
    else:
        try:
            program[target] = state['input'].pop(0)
        except IndexError:
            return True, 9999
    return True, 1


def output_op(program, state, parameters, modes):
    """Output operation."""
    value = program[parameters[0]] if modes[0] == 0 else parameters[0]
    state['output'].append(value)
    # print('output:', state['output'])
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
