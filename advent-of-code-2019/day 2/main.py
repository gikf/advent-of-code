"""Advent of Code 2019 Day 2."""


def main(file_input='input.txt'):
    intcodes = [
        int(num)
        for num in get_file_contents(file_input)[0].strip().split(',')]
    program_alarm = intcodes[:]
    program_alarm[1:3] = [12, 2]
    ending_program = process_program(program_alarm)
    print(f'Value at position 0 after program ends: {ending_program[0]}')
    wanted_num = 19690720
    noun, verb = find_noun_and_verb(intcodes, wanted_num)
    print(f'Result of 100 * noun + verb for program producing {wanted_num}: '
          f'{100 * noun + verb}')


def find_noun_and_verb(program, wanted_number):
    """Find noun and verb seed values to get wanted_number at position 0."""
    val1 = 0
    val2 = 0
    while True:
        next_program = program[:]
        next_program[1:3] = [val1, val2]
        finished_program = process_program(next_program)
        if finished_program[0] == wanted_number:
            noun = val1
            verb = val2
            break
        elif finished_program[0] > wanted_number or val2 >= 144:
            val1 += 1
            val2 = 0
        else:
            val2 += 1
    return noun, verb


def process_program(program):
    """Process program."""
    position = 0
    while True:
        start = position * 4
        end = start + 4
        opcode, pos1, pos2, target = program[start:end]
        opfunc = get_operation(opcode)
        if opfunc is None:
            break
        values = [program[pos] for pos in (pos1, pos2)]
        program[target] = opfunc(*values)
        position += 1
    return program


def get_operation(opcode):
    """Opcode to operation function mapping."""
    opcodes = {
        1: lambda val1, val2: int.__add__(val1, val2),
        2: lambda val1, val2: int.__mul__(val1, val2),
    }
    return opcodes.get(opcode)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
