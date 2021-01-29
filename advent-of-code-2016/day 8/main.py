"""Advent of Code 2016 Day 8."""
import re


ON = '#'
OFF = '.'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    screen = [[OFF for _ in range(50)] for _ in range(6)]
    light(screen, instructions)
    pixels_on = count_pixels_on(screen)
    print(f'Number of pixels on: {pixels_on}')
    print_screen(screen)


def print_screen(screen):
    """Print screen splitting it in half."""
    for part in range(2):
        for row in screen:
            print(row[part * 25:part*25 + 25])
        print()


def light(screen, instructions):
    """Light pixels on screen according to instructions."""
    for func, params in instructions:
        func(screen, *params)


def rotate_row(screen, row, by):
    """Rotate row on screen by number of pixels."""
    row_length = len(screen[row])
    screen[row] = screen[row][row_length - by:] + screen[row][:row_length - by]


def rotate_column(screen, column, by):
    """Rotate column on screen by number of pixels."""
    complete_column = []
    for row in screen:
        complete_column.append(row[column])
    complete_column = (complete_column[len(complete_column) - by:]
                       + complete_column[:len(complete_column) - by])
    for index, _ in enumerate(screen):
        screen[index][column] = complete_column[index]


def rect(screen, columns, rows):
    """Create on screen rectangle from top-left corner.

    Size of rectangle is columns x rows.
    """
    for row in range(rows):
        for column in range(columns):
            screen[row][column] = ON


def count_pixels_on(screen):
    """Count number of pixels ON on screen."""
    return sum(row.count(ON) for row in screen)


def parse_instructions(lines):
    """Parse lines to instructions."""
    return [parse_instruction(line)
            for line in lines]


def parse_instruction(line):
    """Parse line to instruction tuple with function and int parameters."""
    regexes = {
        'rect': (r'(\d+)x(\d+)', rect),
        'rotate row': (r'(\d+) by (\d+)', rotate_row),
        'rotate column': (r'(\d+) by (\d+)', rotate_column),
    }
    for start, (regex, func) in regexes.items():
        if line.startswith(start):
            return (
                func, tuple(int(num) for num in re.findall(regex, line)[0]))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
