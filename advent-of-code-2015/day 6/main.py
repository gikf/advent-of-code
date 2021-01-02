"""Advent of Code 2015 Day 6."""
from functools import lru_cache


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    grid = get_grid(1000, False)
    set_grid(grid, instructions, get_switch_actions())
    print(f'Number of lights on: {get_number_lights_on(grid)}')
    grid = get_grid(1000, 0)
    set_grid(grid, instructions, get_brightness_actions())
    print(f'Total brightness of lights: {get_brightness(grid)}')


def set_grid(grid, instructions, actions):
    """Set grid according to instructions, with actions."""
    for instruction, [corner1, corner2] in instructions:
        action = select_action(instruction, actions)
        for coordinates in get_rectangle_from_corners(corner1, corner2):
            column, row = coordinates
            action(row, column, grid)


def select_action(instruction, actions):
    """Return function cooresponding to the instruction from actions dict."""
    return actions[instruction]


def get_switch_actions():
    """Actions for switch grid."""
    return {
        'turn on': turn_on,
        'turn off': turn_off,
        'toggle': toggle,
    }


def get_brightness_actions():
    """Actions for brightness grid."""
    return {
        'turn on': increase_brightness,
        'turn off': decrease_brightness,
        'toggle': toggle_brightness,
    }


def increase_brightness(row, column, grid):
    """Increases brightness by 1."""
    change_brightness(row, column, grid, 1)


def decrease_brightness(row, column, grid):
    """Decrease brightness by 1, with minimum of 0."""
    if grid[row][column] > 0:
        change_brightness(row, column, grid, -1)


def toggle_brightness(row, column, grid):
    """Toggle brightness - increase brightness by 2."""
    change_brightness(row, column, grid, 2)


def change_brightness(row, column, grid, value):
    """Change brightness light at row, column in grid, by value."""
    grid[row][column] += value


@lru_cache()
def get_rectangle_from_corners(corner1, corner2):
    """Get coordinates of rectangle created from two opposite corners."""
    row1, col1 = corner1
    row2, col2 = corner2
    coordinates = []
    for row in range(row1, row2 + 1):
        for col in range(col1, col2 + 1):
            coordinates.append((row, col))
    return coordinates


def parse_instructions(lines):
    """Parse instructions from lines."""
    return [
        parse_instruction(instruction)
        for instruction in lines
    ]


def parse_instruction(instruction):
    """Parse string instruction to representation of instruction.

    'toggle 173,401 through 496,407' -> ('toggle', [(173, 401), (496, 407)])
    """
    instruction, corner2 = instruction.split(' through ')
    instruction, corner1 = instruction.rsplit(maxsplit=1)
    return instruction, [tuple([int(num)for num in coordinates.split(',')])
                         for coordinates in (corner1, corner2)]


def toggle(row, column, grid):
    """Toggle light at row, column in grid."""
    if grid[row][column]:
        turn_off(row, column, grid)
    else:
        turn_on(row, column, grid)


def turn_off(row, column, grid):
    """Turn off light at row, column in grid."""
    set_light(row, column, grid, False)


def turn_on(row, column, grid):
    """Turn on light at row, column in grid."""
    set_light(row, column, grid, True)


def set_light(row, column, grid, value):
    """Set row, column in grid to value."""
    grid[row][column] = value


def get_brightness(grid):
    """Get total brightness in grid."""
    return sum(sum(row) for row in grid)


def get_number_lights_on(grid):
    """Get number of lights on in grid."""
    return sum(row.count(True) for row in grid)


def get_grid(size, value):
    """Get square grid of size, with default value."""
    return [
        [value for _ in range(size)]
        for _ in range(size)
    ]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
