"""Advent of Code 2017 Day 5."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    jumps = [int(num) for num in lines]
    adjusts = (
        (increase, 'increases offset by 1'),
        (decrease_when_higher_than_3,
         'decreases offset when higher or equal 3'
         'else increases by 1')
    )
    for offset_adjust, description in adjusts:
        steps = make_jumps(jumps, offset_adjust)
        print(f'Number of steps to exit when adjust {description}: {steps}')


def make_jumps(jumps, offset_adjust):
    """Process jumps, using offset_adjust function to adjust offset value."""
    cur_jumps = jumps[:]
    jump_count = 0
    cur_index = 0
    while 0 <= cur_index < len(cur_jumps):
        jump_count += 1
        offset_value = cur_jumps[cur_index]
        next_index = cur_index + offset_value
        cur_jumps[cur_index] += offset_adjust(offset_value)
        cur_index = next_index
    return jump_count


def increase(_):
    """Return offset adjust 1."""
    return 1


def decrease_when_higher_than_3(offset):
    """Return offset adjust -1 if offset >= 3, otherwise return 1."""
    return -1 if offset >= 3 else 1


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
