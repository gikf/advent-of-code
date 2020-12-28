# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:35:54 2020
"""


def main():
    instructions = [line.strip() for line in get_file_contents()]
    for index, line in enumerate(instructions):
        starts_with_jmp = line.startswith('jmp')
        starts_with_nop = line.startswith('nop')
        if not any((starts_with_jmp, starts_with_nop)):
            continue
        new_instructions = instructions[:]

        if starts_with_jmp:
            new_instructions[index] = line.replace('jmp', 'nop')
        elif starts_with_nop:
            new_instructions[index] = line.replace('nop', 'jmp')

        if process_instructions(new_instructions) is not None:
            print(f'Changed line: {index}')
            break


def process_instructions(instructions):
    """Process instructions in order, starting from line 0"""
    line = 0
    instructions_executed = set()
    accumulator = 0
    while line not in instructions_executed:
        try:
            instruction = instructions[line]
        except IndexError:
            print(f'End encountered, accumulator: {accumulator}')
            return accumulator
        instructions_executed.add(line)
        line, accumulator = process_instruction(instruction, line, accumulator)
    return None


def process_instruction(instruction, line, accumulator):
    """Process operation from single instruction."""
    operations = {
        'nop': lambda l, diff: (line + 1, accumulator),
        'acc': lambda l, diff: (line + 1, accumulator + diff),
        'jmp': lambda l, diff: (line + diff, accumulator),
    }
    operation, operation_diff = instruction.split()
    return operations[operation](line, int(operation_diff))


def get_file_contents(file="input.txt"):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
