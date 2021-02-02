"""Advent of Code 2016 Day 12."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    register = get_empty_register()
    instructions = parse_instructions(lines)
    processed_register = process(register, instructions)
    print(f"Value in register a: {processed_register['a']}")
    register['c'] = 1
    processed_register_seeded = process(register, instructions)
    print("Value in register a, after seeding register c at start with 1: "
          f"{processed_register_seeded['a']}")


def process(register, instructions):
    """Process instructions on copy of register."""
    cur_register = register.copy()
    cur_index = 0
    while cur_index < len(instructions):
        cur_instruction = instructions[cur_index]
        cur_index += process_instruction(cur_register, cur_instruction)
    return cur_register


def process_instruction(register, instruction):
    """Process instruction on register.

    Returns change of instruction index."""
    name, *params = instruction
    func = get_operation(name)
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
        return jump_by


def get_operation(name):
    """Get operation function for name."""
    return {
        'cpy': operation_cpy,
        'inc': operation_inc,
        'dec': operation_dec,
        'jnz': operation_jnz,
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
