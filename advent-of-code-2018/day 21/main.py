"""Advent of Code 2018 Day 21."""
import operator


def main(file_input='input.txt'):
    register_line, *lines = [
        line.strip() for line in get_file_contents(file_input)]
    program = parse_program(lines)
    instruction_pointer = int(register_line[-1])
    seed = find_seed(program, instruction_pointer)
    print('Lowest integer in register 0 making program stop after executing '
          f'the fewest instructions: {seed}')
    seed = part2()
    print('Lowest integer in register 0 making program stop after executing '
          f'the most instructions: {seed}')


def part2():
    """Find seed halting program after executing the most instructions."""
    # https://www.reddit.com/r/adventofcode/comments/a86jgt/2018_day_21_solutions/ec9f09d/
    registers = [0 for _ in range(6)]
    seen = set()
    counter = 0
    prev_register = None
    while True:
        registers[4] = registers[1] | 65536
        registers[1] = 12772194
        while True:
            registers[1] += registers[4] & 255
            registers[1] = registers[1] & 16777215
            registers[1] = registers[1] * 65899
            registers[1] = registers[1] & 16777215
            if 256 > registers[4]:
                if registers[1] in seen:
                    registers[1] = prev_register
                    return prev_register
                prev_register = registers[1]
                seen.add(registers[1])
                break
            registers[4] = registers[4] // 256
        counter += 1


def find_seed(program, instruction_pointer):
    """Find seed halting program after executing fewest instructions."""
    registers = [0 for _ in range(6)]
    end_registers = execute(
        registers, program, instruction_pointer)
    seed = end_registers[1]
    return seed


def execute(registers, program, pointer_register):
    """Execute program on based on op_codes op_code -> operation mapping."""
    pointer = 0
    while pointer < len(program):
        registers[pointer_register] = pointer
        operation, values = program[pointer]
        if pointer == 28:
            return registers
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
