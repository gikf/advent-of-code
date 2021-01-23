"""Advent of Code 2016 Day 2."""

EMPTY = '#'
moves = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}


def main(file_input='input.txt'):
    instructions = [line.strip() for line in get_file_contents(file_input)]
    keypad = ['123',
              '456',
              '789']
    code = get_keypad_code(keypad, instructions)
    print(code)
    bathroom_keypad = ['##1##',
                       '#234#',
                       '56789',
                       '#ABC#',
                       '##D##']
    bathroom_code = get_keypad_code(bathroom_keypad, instructions)
    print(bathroom_code)


def get_keypad_code(keypad, instructions):
    """Get code for keypad based on instructions."""
    code = []
    last_position = [1, 1]
    for instruction in instructions:
        position = get_next_position(keypad, last_position, instruction)
        row, column = position
        code.append(keypad[row][column])
        last_position = position
    return ''.join(code)


def get_next_position(keypad, position, instruction):
    """Get next position on keypad based on start position and instruction."""
    for move in instruction:
        next_position = []
        for coordinate, change in zip(position, moves[move]):
            next_position.append(
                get_coordinate(coordinate, change, len(keypad)))
        row, col = next_position
        if keypad[row][col] == EMPTY:
            continue
        position = next_position
    return position


def get_coordinate(coordinate, change, limit):
    """Get next coordinate, within 0 and limit."""
    next_coordinate = coordinate + change
    if next_coordinate < 0:
        return 0
    elif next_coordinate >= limit:
        return limit - 1
    return next_coordinate


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
