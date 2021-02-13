"""Advent of Code 2016 Day 23."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    register = get_empty_register()
    for seed_number in [7, 12]:
        instructions = parse_instructions(lines)
        register['a'] = seed_number
        processed_register = process(register, instructions)
        print('Value in register a, after seeding register a with '
              f"{seed_number}: {processed_register['a']}")


def process(register, instructions):
    """Process instructions on copy of register."""
    cur_register = register.copy()
    cur_index = 0
    while cur_index < len(instructions):
        cur_instruction = instructions[cur_index]
        # Hand optimization shorting long loop incrementing and decrementing
        if cur_index in [5, 21]:
            cur_register['a'] += cur_register['d'] * cur_register['c']
            cur_register['c'] = 1 if cur_index == 21 else 0
            cur_register['d'] = 0 if cur_index == 21 else 1
            cur_index += 2
        else:
            cur_index += process_instruction(
                cur_register, instructions, cur_instruction, cur_index)
    return cur_register


def process_instruction(register, instructions, instruction, cur_index):
    """Process instruction on register.

    Returns change of instruction index."""
    name, *params = instruction
    func = get_operation(name)
    if func == operation_tgl:
        result = func(register, instructions, cur_index, *params)
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


def operation_tgl(register, instructions, index, target):
    """Toggles relative target.

    - For one-argument instructions, inc becomes dec, and all
        other one-argument instructions become inc.
    - For two-argument instructions, jnz becomes cpy, and all other
        two-instructions become jnz.
    - The arguments of a toggled instruction are not affected.
    - If an attempt is made to toggle an instruction outside the program,
        nothing happens.
    - If toggling produces an invalid instruction (like cpy 1 2) and an attempt
        is later made to execute that instruction, skip it instead.
    - If tgl toggles itself (for example, if a is 0, tgl a would target itself
        and become inc a), the resulting instruction is not executed until the
        next time it is reached.
    """
    target_index = index + register[target]
    try:
        target_instruction, *params = instructions[target_index]
        instructions[target_index][0] = toogles(target_instruction)
    except IndexError:
        pass


def toogles(name):
    return {
        'inc': 'dec',
        'dec': 'inc',
        'tgl': 'inc',
        'jnz': 'cpy',
        'cpy': 'jnz',
    }[name]


def get_operation(name):
    """Get operation function for name."""
    return {
        'cpy': operation_cpy,
        'inc': operation_inc,
        'dec': operation_dec,
        'jnz': operation_jnz,
        'tgl': operation_tgl,
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
