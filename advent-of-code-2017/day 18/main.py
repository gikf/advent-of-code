"""Advent of Code 2017 Day 18."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    register = get_register()
    process_instructions(register, instructions)
    print(f"Last recovered frequency: {register['sound'][-1]}")
    registers = run_programs(instructions)
    print(f"Number of messages send by program 1: {registers[1]['counter']}")


def run_programs(instructions):
    """Run two programs sending and receiving from each other."""
    register0 = get_register()
    register0['p'] = 0
    register1 = get_register()
    register1['p'] = 1
    registers = {0: register0, 1: register1}
    cur_instructions = [0, 0]
    while not is_deadlock(registers, cur_instructions, instructions):
        for index, instruction in enumerate(cur_instructions):
            name, params = instructions[instruction]
            if name == 'rcv':
                cur_instructions[index] = receive(
                    registers[index],
                    cur_instructions[index],
                    *params,
                    registers[(index + 1) % 2]
                )
            else:
                func = get_func(name)
                cur_instructions[index] = func(
                    registers[index], cur_instructions[index], *params)
            cur_instructions[index] += 1
    return registers


def get_register():
    """Get empty register."""
    register = defaultdict(int)
    register['sound'] = []
    return register


def is_deadlock(registers, cur_instructions, instructions):
    """Check if programs are in deadlock."""
    for index, cur_instruction in enumerate(cur_instructions):
        if not (is_receiving(instructions[cur_instruction])
                and is_queue_empty(registers[(index + 1) % 2])):
            return False
    return True


def is_queue_empty(register):
    """Check if send queue is empty."""
    return len(register['sound']) == 0


def is_receiving(instruction):
    """Check if instruction is receiving."""
    return instruction[0] == 'rcv'


def process_instructions(register, instructions, registers=None):
    """Process instructions."""
    cur_instruction = 0
    while 0 <= cur_instruction < len(instructions):
        name, params = instructions[cur_instruction]
        func = get_func(name)
        cur_instruction = func(register, cur_instruction, *params)
        cur_instruction += 1
    return register


def play_sound(register, cur_instruction, name):
    """Play sound/send instruction."""
    register['sound'].append(register[name])
    register['counter'] += 1
    return cur_instruction


def set_register(register, cur_instruction, target, source):
    """Set instruction."""
    register[target] = source if is_int(source) else register[source]
    return cur_instruction


def increase_by(register, cur_instruction, target, source):
    """Increase instruction."""
    register[target] += source if is_int(source) else register[source]
    return cur_instruction


def multiply(register, cur_instruction, target, source):
    """Multiply instruction."""
    register[target] *= source if is_int(source) else register[source]
    return cur_instruction


def remainder(register, cur_instruction, target, source):
    """Remainder instruction."""
    modulo = (
        register[target] % (source if is_int(source) else register[source]))
    register[target] = modulo
    return cur_instruction


def receive(register, cur_instruction, target, other_register):
    """Receive instruction."""
    try:
        register[target] = other_register['sound'].pop(0)
    except IndexError:
        return cur_instruction - 1
    return cur_instruction


def recover(register, cur_instruction, source):
    """Recover instruction."""
    value = source if is_int(source) else register[source]
    if value != 0:
        return 150
    return cur_instruction


def jump(register, cur_instruction, source, offset):
    """Jump instruction."""
    value = source if is_int(source) else register[source]
    offset = offset if is_int(offset) else register[offset]
    if value > 0:
        return cur_instruction + offset - 1
    return cur_instruction


def is_int(item):
    """Check if item is int."""
    return isinstance(item, int)


def get_func(name):
    """Instruction name to function mapping."""
    return {
        'snd': play_sound,
        'set': set_register,
        'add': increase_by,
        'mul': multiply,
        'mod': remainder,
        'rcv': recover,
        'jgz': jump,
    }[name]


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
