"""Advent of Code 2018 Day 19."""
import operator


def main(file_input='input.txt'):
    register_line, *lines = [
        line.strip() for line in get_file_contents(file_input)]

    program = parse_program(lines)
    instruction_pointer = int(register_line[-1])
    registers = [0 for _ in range(6)]
    end_registers = execute(registers, program, instruction_pointer)
    print(f'Final value in register 0: {end_registers[0]}')
    registers = [1] + [0 for _ in range(5)]
    end_registers = execute(registers, program, instruction_pointer)
    print('Final value in register 0 when starting with 1 in register 0 '
          f'{end_registers[0]}')


def execute(registers, program, pointer_register):
    """Execute program on based on op_codes op_code -> operation mapping."""
    pointer = 0
    while pointer < len(program):
        registers[pointer_register] = pointer
        operation, values = program[pointer]
        if pointer == 2 and registers[2] != 0:
            if registers[1] % registers[2] == 0:
                registers[0] += registers[2]
            registers[3] = 0
            registers[5] = registers[1]
            pointer = 12
            continue
        registers = caller(operation, registers, values)
        pointer = registers[pointer_register] + 1
    return registers


def caller(operation, registers, params):
    """Call function based on operation on registers and parameters."""
    operations = get_call_operations()
    func, get_params, *rest = operations[operation]
    return func(registers, *get_params(registers, params), *rest)


def register_param(registers, params):
    """Return from registers register parameters."""
    return registers[params[0]], registers[params[1]], params[2]


def set_register_param(registers, params):
    """Return from registers register parameters for set action."""
    return registers[params[0]], params[1], params[2]


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
        'setr': (set_action, set_register_param),
        'seti': (set_action, lambda register, params: params),
        'gtir': (compare_action, compare_ir_param, operator.gt),
        'gtri': (compare_action, compare_ri_param, operator.gt),
        'gtrr': (compare_action, compare_rr_param, operator.gt),
        'eqir': (compare_action, compare_ir_param, operator.eq),
        'eqri': (compare_action, compare_ri_param, operator.eq),
        'eqrr': (compare_action, compare_rr_param, operator.eq),
    }


def parse_program(lines):
    """Parse lines to list of lists with instruction name and values for it."""
    program = []
    for line in lines:
        name, nums = line.split(maxsplit=1)
        program.append((name, [int(num) for num in nums.split()]))
    return program


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
