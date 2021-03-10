"""Advent of Code 2017 Day 23."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    register = {letter: 0 for letter in 'abcdefgh'}
    register = process_instructions(register, instructions)
    print(f'Times mul instruction executed: {multiply.counter}')
    register = {letter: 0 for letter in 'abcdefgh'}
    register['a'] = 1
    h_value = process_stage_2(register)
    print(f'Value in register h after seeding register a with 1: {h_value}')


def process_stage_2(register):
    """Return register after processing stage 2."""
    # After exploring https://www.reddit.com/r/adventofcode/comments/7lms6p/2017_day_23_solutions/drnmlbk/
    b = 57 * 100 + 100_000
    c = b + 17000
    h = 0
    for cur_num in range(b, c + 1, 17):
        for d in range(2, cur_num):
            if cur_num % d == 0:
                h += 1
                break
    return h


def count_wrapper(func):
    """Wrapper counting numbers of calls."""
    def wrap(*args, **kwargs):
        wrap.counter += 1
        return func(*args, **kwargs)
    wrap.counter = 0
    return wrap


def process_instructions(register, instructions, registers=None):
    """Process instructions."""
    cur_instruction = 0
    while 0 <= cur_instruction < len(instructions):
        name, params = instructions[cur_instruction]
        func = get_func(name)
        cur_instruction = func(register, cur_instruction, *params)
        cur_instruction += 1
    return register


def get_func(name):
    """Instruction name to function mapping."""
    return {
        'set': set_register,
        'sub': decrease_by,
        'mul': multiply,
        'jnz': jump,
    }[name]


def set_register(register, cur_instruction, target, source):
    """Set instruction."""
    register[target] = get_value(register, source)
    return cur_instruction


def decrease_by(register, cur_instruction, target, source):
    """Increase instruction."""
    register[target] -= get_value(register, source)
    return cur_instruction


@count_wrapper
def multiply(register, cur_instruction, target, source):
    """Multiply instruction."""
    register[target] *= get_value(register, source)
    return cur_instruction


def jump(register, cur_instruction, source, offset):
    """Jump instruction."""
    value = get_value(register, source)
    offset = get_value(register, offset)
    if value != 0:
        return cur_instruction + offset - 1
    return cur_instruction


def get_value(register, source):
    """Get source value, if it's not integer return it from register."""
    return source if is_int(source) else register[source]


def is_int(item):
    """Check if item is int."""
    return isinstance(item, int)


def parse_instructions(lines):
    """Parse lines to list of instructions."""
    return [parse_instruction(line) for line in lines]


def parse_instruction(line):
    """Parse line to tuple with instruction name and parameters list."""
    name, *params = line.split()
    return (name, [param if param.isalpha() else int(param)
                   for param in params])


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
