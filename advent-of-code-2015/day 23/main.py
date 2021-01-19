"""Advent of Code 2015 Day 23."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    register = process(instructions, {'a': 0, 'b': 0})
    print(f"Value of b after finishing execution: {register['b']}")
    register_stage2 = process(instructions, {'a': 1, 'b': 0})
    print('Value of b after finishing execution, when a started as 1: '
          f"{register_stage2['b']}")


def process(instructions, register):
    """Process instructions with starting register."""
    cur_position = 0
    while cur_position < len(instructions):
        to_process, *params = instructions[cur_position]
        result = process_instruction(register,
                                     cur_position,
                                     to_process,
                                     *params)
        if result is not None:
            cur_position = result
        else:
            cur_position += 1
    return register


def process_instruction(register, cur_position, instruction, *params):
    """Process instruction on register or cur_position."""
    instructions = {
        'hlf': (hlf, (register, *params)),
        'tpl': (tpl, (register, *params)),
        'inc': (inc, (register, *params)),
        'jmp': (jmp, (cur_position, *params)),
        'jie': (jie, (register, cur_position, *params)),
        'jio': (jio, (register, cur_position, *params)),
    }
    to_process, arguments = instructions[instruction]
    return to_process(*arguments)


def hlf(register, reg_name):
    """Divide by two reg_name value in register."""
    set_register(register, reg_name, register[reg_name] / 2)


def tpl(register, reg_name):
    """Triple reg_name value in register."""
    set_register(register, reg_name, register[reg_name] * 3)


def inc(register, reg_name):
    """Increase by one reg_name value in register."""
    set_register(register, reg_name, register[reg_name] + 1)


def jmp(cur_position, value_change):
    """Jump relatively from cur_position by value_change."""
    return cur_position + value_change


def jie(register, cur_instruction, reg_name, value_change):
    """Jump if even instruction."""
    if register[reg_name] % 2 == 0:
        return jmp(cur_instruction, value_change)


def jio(register, cur_instruction, reg_name, value_change):
    """Jump if one instruction."""
    if register[reg_name] == 1:
        return jmp(cur_instruction, value_change)


def set_register(register, reg_name, value):
    """Set value for reg_name in register."""
    register[reg_name] = value


def parse_instructions(lines):
    """Parse lines to instructions."""
    return [parse_instruction(line) for line in lines]


def parse_instruction(line):
    """Parse line with instruction to tuple representing it."""
    instruction, element, *parts = line.split()
    if parts:
        return (instruction, element[:-1], int(parts[0]))
    if element.isalpha():
        return (instruction, element)
    return (instruction, int(element))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
