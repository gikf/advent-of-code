"""Advent of Code 2021 Day 2."""


def main(file_input='input.txt'):
    course = [parse_line(line) for line in get_file_contents(file_input)]
    funcs = {
        'forward': lambda params, value: change_param(
            params, 'position', value),
        'down': lambda params, value: change_param(params, 'depth', value),
        'up': lambda params, value: change_param(params, 'depth', -value),
    }
    depth, position = follow_course(course, funcs)
    print(f'Multiplication of depth and final position: {depth * position}')

    funcs = {
        'forward': forward,
        'down': lambda values, value: change_param(values, 'aim', value),
        'up': lambda values, value: change_param(values, 'aim', -value),
    }
    depth, position = follow_course(course, funcs)
    print('Multiplication of depth and final position, with consideration of '
          f'aim: {depth * position}')


def forward(paramters, value):
    """Forward course instruction, with aim consideration."""
    paramters['position'] += value
    paramters['depth'] += paramters['aim'] * value


def change_param(parameters, parameter, value):
    """Change param in params by the change value."""
    parameters[parameter] += value


def follow_course(course, funcs):
    """Follow course, using the funcs."""
    parameters = {
        'depth': 0,
        'position': 0,
        'aim': 0,
    }
    for instruction, value in course:
        func = funcs[instruction]
        func(parameters, value)
    return parameters['depth'], parameters['position']


def parse_line(line):
    """Parse line to (instruction, value) tuple."""
    return [int(part) if part.isdigit() else part for part in line.split()]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
