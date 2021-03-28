"""Advent of Code 2018 Day 16."""
from collections import defaultdict
import operator
import re


def main(file_input='input.txt'):
    sample_lines, program_lines = get_file_contents(file_input).split('\n\n\n')
    possible_ops = get_possible_ops(parse_samples(sample_lines))

    three_or_more_ops = [
        op_count for op_count, sample in possible_ops if len(op_count) >= 3]
    print('Samples with three or more possible opcodes: '
          f'{len(three_or_more_ops)}')

    op_codes = find_op_codes(possible_ops)
    result = execute(op_codes, parse_program(program_lines))
    print(f'Value in register 0 after executing program: {result[0]}')


def execute(op_codes, program):
    """Execute program on based on op_codes op_code -> operation mapping."""
    registers = [0 for _ in range(4)]
    for instruction in program:
        op_code, *values = instruction
        registers = caller(op_codes[op_code], registers, values)
    return registers


def find_op_codes(possible_ops):
    """Find mapping op_code -> operation, from possible_ops."""
    op_codes = {}
    code_to_operations = defaultdict(set)
    for operations, code in possible_ops:
        for operation in operations:
            code_to_operations[code].add(operation)
    while len(op_codes) < 16:
        codes_by_possible_operations = sorted(
            code_to_operations, key=lambda item: len(code_to_operations[item]))
        for code in codes_by_possible_operations:
            cur_operations = code_to_operations[code]
            if len(cur_operations) != 1:
                continue
            operation = cur_operations.pop()
            op_codes[code] = operation
            code_to_operations = remove_from_values(
                code_to_operations, operation)
            del code_to_operations[code]
    return op_codes


def remove_from_values(dictionary, to_remove):
    """Remove to_remove value from values in dictionary."""
    for key, values in dictionary.items():
        if to_remove in values:
            dictionary[key] = values - {to_remove}
    return dictionary


def get_possible_ops(samples):
    """Get possible operations for codes from samples."""
    ops = []
    for sample in samples:
        cur_ops = set()
        instruction, before, after = sample
        op_code, *registers = instruction
        for operation in get_operations():
            result = caller(operation, before[:], registers)
            if result == after:
                cur_ops.add(operation)
        ops.append((cur_ops, instruction[0]))
    return ops


def caller(operation, registers, params):
    """Call function based on operation on registers and parameters."""
    operations = get_call_operations()
    func, get_params, *rest = operations[operation]
    return change_action(registers, *get_params(registers, params), *rest)


def register_param(registers, params):
    """Return from registers register parameters."""
    return registers[params[0]], registers[params[1]], params[2]


def immediate_param(registers, params):
    """Return from registers immediate parameters."""
    return registers[params[0]], params[1], params[2]


def compare_ir_param(registers, params):
    """Return From registers immediate/register parameters for compare."""
    return params[0], registers[params[1]], params[2]


def compare_ri_param(registers, params):
    """Return from registers register/immediate parameters for compare."""
    return registers[params[0]], params[1], params[2]


def compare_rr_param(registers, params):
    """Return from registers register parameters for compare action."""
    return registers[params[0]], registers[params[1]], params[2]


def change_action(registers, num_a, num_b, reg_c, operation):
    """Perform change action using operation on num_a and num_b."""
    registers[reg_c] = operation(num_a, num_b)
    return registers


def set_action(registers, num_a, _, reg_c):
    """Perform assign action of num_a to reg_c in registers."""
    registers[reg_c] = num_a
    return registers


def compare_action(registers, num_a, num_b, reg_c, operation):
    """Perform compare action of operation on num_a and num_b."""
    registers[reg_c] = 1 if operation(num_a, num_b) else 0
    return registers


def get_operations():
    """Get possible operations."""
    return (
        'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
    )


def get_call_operations():
    """Get operations to operation parameters mapping for caller."""
    return {
        'addr': (change_action, register_param, operator.add),
        'addi': (change_action, immediate_param, operator.add),
        'mulr': (change_action, register_param, operator.mul),
        'muli': (change_action, immediate_param, operator.mul),
        'banr': (change_action, register_param, operator.and_),
        'bani': (change_action, immediate_param, operator.and_),
        'borr': (change_action, register_param, operator.or_),
        'bori': (change_action, immediate_param, operator.or_),
        'setr': (set_action, register_param),
        'seti': (set_action, lambda register, params: params),
        'gtir': (compare_action, compare_ir_param, operator.gt),
        'gtri': (compare_action, compare_ri_param, operator.gt),
        'gtrr': (compare_action, compare_rr_param, operator.gt),
        'eqir': (compare_action, compare_ir_param, operator.eq),
        'eqri': (compare_action, compare_ri_param, operator.eq),
        'eqrr': (compare_action, compare_rr_param, operator.eq),
    }


def parse_program(lines):
    """Parse program from lines."""
    return [[int(num) for num in line.strip().split()]
            for line in lines.strip().split('\n')]


def parse_samples(lines):
    """Parse lines to sample representation - tuple with three lists."""
    samples = []
    regex = r'\[(\d+), (\d+), (\d+), (\d+)\]'
    for single_sample in lines.split('\n\n'):
        before, codes, after = single_sample.split('\n')
        before = [int(num) for num in re.findall(regex, before)[0]]
        codes = [int(num) for num in codes.split()]
        after = [int(num) for num in re.findall(regex, after)[0]]
        samples.append((codes, before, after))
    return samples


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
