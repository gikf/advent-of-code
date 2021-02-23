"""Advent of Code 2017 Day 8."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    register = defaultdict(int)
    processed_register, moment_max = process_instructions(
        register.copy(), instructions)
    maximum = get_max_value(processed_register)
    print(f'Highest value in register at the end: {maximum}')
    print(f'Highest value held at any point: {moment_max}')


def process_instructions(register, instructions):
    """Process instructions on register."""
    intermediate_max = 0
    for modifier, condition in instructions:
        check_name, check_function, check_value = condition
        if not check_function(register[check_name], check_value):
            continue
        name, modify, value = modifier
        modify(register, name, value)
        intermediate_max = max(intermediate_max, get_max_value(register))
    return register, intermediate_max


def get_max_value(register):
    """Get maximum value from register."""
    return max(register.values())


def get_action_function(action):
    """Return action function corresponding to action."""
    return {
        'inc': increase,
        'dec': decrease,
    }[action]


def get_check_function(check):
    """Return check function corresponding to check."""
    return {
        '>': int.__gt__,
        '<': int.__lt__,
        '>=': int.__ge__,
        '==': int.__eq__,
        '<=': int.__le__,
        '!=': int.__ne__,
    }[check]


def increase(register, name, value):
    """Increase name in register by value."""
    register[name] += value


def decrease(register, name, value):
    """Decrease name in register by value."""
    increase(register, name, -value)


def parse_instructions(lines):
    """Parse instructions form lines."""
    return [parse_instruction(line) for line in lines]


def parse_instruction(line):
    """Parse line to instruction."""
    modifier, condition = [part.split() for part in line.split(' if ')]
    return parse_modifier(modifier), parse_condition(condition)


def parse_condition(condition):
    """Parse condition part, return list with name, function and number."""
    return [func(value) for value, func in zip(
        condition, (lambda x: x, get_check_function, int))]


def parse_modifier(modifier):
    """Parse modifier part, return list with name, function and number."""
    return [func(value) for value, func in zip(
        modifier, (lambda x: x, get_action_function, int))]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
