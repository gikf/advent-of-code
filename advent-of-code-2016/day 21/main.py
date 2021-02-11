"""Advent of Code 2016 Day 21."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    to_scramble = 'abcdefgh'
    scrambled_password = ''.join(scramble(list(to_scramble), instructions))
    print(f'Scrambled {to_scramble}: {scrambled_password}')
    to_unscramble = 'fbgdceah'
    unscrambled = ''.join(unscramble(list(to_unscramble), instructions))
    print(f'Unscrambled {to_unscramble}: {unscrambled}')


def unscramble(password, instructions):
    """Unscramble password by reversing instructions."""
    for func, params in instructions[::-1]:
        if func == move:
            function_params = [*params[::-1]]
        elif func == rotate:
            rotate_type, param1, param2 = params
            if rotate_type == 'based':
                param1 = find_rotation(password, *params)
            function_params = [change_rotation(rotate_type), param1, param2]
        else:
            function_params = [*params]
        password = func(password, *function_params)
    return password


def change_rotation(rotation_type):
    """Change rotation to reverse it."""
    return {
        'right': 'left',
        'left': 'right',
        'based': 'left'
    }[rotation_type]


def find_rotation(password, *params):
    """Find rotation resulting in password"""
    _, _, letter = params
    wanted_index = password.index(letter)
    for index, _ in enumerate(password):
        to_rotate = '{}{}{}'.format(
            ('.' * index),
            letter,
            ('.' * (len(password) - index - 1)))
        after_rotation = rotate(to_rotate, *params)
        if after_rotation.index(letter) == wanted_index:
            return wanted_index - index


def scramble(password, instructions):
    """Scramble password using instructions."""
    for func, params in instructions:
        password = func(password[:], *params)
    return password


def move(password, position_x, position_y):
    """Move letter from position_x to position_y.

    Letter should be removed from password and inserted at position_y.
    """
    to_move = password.pop(position_x)
    password.insert(position_y, to_move)
    return password


def swap(password, swap_type, position_x, position_y):
    """Swap position_x and position_y.

    If swap_type is 'letter' swap indices of corresponding letters.
    """
    if swap_type == 'letter':
        position_x = password.index(position_x)
        position_y = password.index(position_y)
    password[position_x], password[position_y] = (password[position_y],
                                                  password[position_x])
    return password


def rotate(password, rotate_type, *params):
    """Rotate password

    - rotate left/right X steps - means that the whole string
        should be rotated; for example, one right rotation would turn
        abcd into dabc.
    - rotate based on position of letter X - means that the whole string should
        be rotated to the right based on the index of letter X (counting
        from 0) as determined before this instruction does any rotations.
        Once the index is determined, rotate the string to the right one time,
        plus a number of times equal to that index, plus one additional time
        if the index was at least 4.
    """
    if isinstance(params[0], int):
        steps = params[0]
    else:
        index = password.index(params[1])
        steps = index + 1
        if index >= 4:
            steps += 1
    if rotate_type != 'left':
        steps = -steps
    steps = steps % len(password)
    return password[steps:] + password[:steps]


def reverse(password, position_x, position_y):
    """Reverse from position_x to position_y in password."""
    password_slice = password[position_x:position_y + 1]
    password[position_x:position_y + 1] = password_slice[::-1]
    return password


def get_funcs(name):
    """Return tuple with instruction function and one getting parameters."""
    funcs = {
        'move': (move, lambda item: (item[1], item[-1])),
        'reverse': (reverse, lambda item: (item[1], item[-1])),
        'swap': (swap, lambda item: (item[0], item[1], item[-1])),
        'rotate': (rotate, lambda item: (item[0], item[1], item[-1])),
    }
    return funcs[name]


def parse_instructions(lines):
    """Parse instructions from lines."""
    return [parse_instruction(line) for line in lines]


def parse_instruction(line):
    """Parse line to instruction with function and parameters."""
    name, *rest = line.split()
    func, get_params_function = get_funcs(name)
    params = [param if param.isalpha() else int(param)
              for param in get_params_function(rest)]
    return func, params


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
