"""Advent of Code 2016 Day 25."""
from collections import deque


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    lowest_seed = find_lowest_seed(instructions)
    print(lowest_seed)


def find_lowest_seed(instructions):
    """Find lowest seed for register "a" to transmit "0, 1" indefinitely."""
    seed = 0
    while True:
        register = get_empty_register()
        register['a'] = seed
        if not process(register, instructions):
            break
        seed += 1
    return seed


def process(register, instructions):
    """Process instructions on copy of register."""
    cur_register = register.copy()
    cur_index = 0
    states = set()
    transmissions = deque()
    while cur_index < len(instructions):
        cur_state = tuple(sorted(cur_register.items())), cur_index
        if cur_state in states:
            return False
        states.add(cur_state)
        cur_instruction = instructions[cur_index]
        cur_index += process_instruction(
            cur_register, cur_instruction, transmissions)
    return cur_register


def process_instruction(register, instruction, transmissions):
    """Process instruction on register.

    Returns change of instruction index."""
    name, *params = instruction
    func = get_operation(name)
    if func == operation_out:
        result = func(register, *params, transmissions)
    else:
        result = func(register, *params)
    return result if isinstance(result, int) else 1


def operation_cpy(register, source, target):
    """Copy source value or register to target register."""
    if isinstance(source, str):
        source = register[source]
    register[target] = source


def operation_inc(register, target):
    """Increase target in register by 1."""
    register[target] += 1


def operation_dec(register, target):
    """Decrease target in register by 1."""
    register[target] -= 1


def operation_jnz(register, register_check, jump_by):
    """Jump operation. Jump if register_check is not 0."""
    if register.get(register_check, register_check) != 0:
        return jump_by if isinstance(jump_by, int) else register[jump_by]


def operation_out(register, source, transmissions):
    """Transmitting operation.

    Returns value ending program when values in transmission don't repeat
    0 and 1 indefinitely.
    """
    if len(transmissions) == 2:
        transmissions.popleft()
    value = register.get(source, source)
    transmissions.append(value)
    if len(transmissions) == 2:
        val_a, val_b = transmissions
        if (val_a == val_b
                or val_a not in {0, 1}
                or val_b not in {0, 1}):
            return 50


def get_operation(name):
    """Get operation function for name."""
    return {
        'cpy': operation_cpy,
        'inc': operation_inc,
        'dec': operation_dec,
        'jnz': operation_jnz,
        'out': operation_out,
    }[name]


def parse_instructions(lines):
    """Parse lines to list of instructions."""
    return [parse_instruction(line)
            for line in lines]


def parse_instruction(line):
    """Parse line to instruction."""
    return [part if part.isalpha() else int(part)
            for part in line.split()]


def get_empty_register():
    """Create empty register."""
    return {'a': 0, 'b': 0, 'c': 0, 'd': 0}


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
