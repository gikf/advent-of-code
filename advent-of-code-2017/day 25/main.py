"""Advent of Code 2017 Day 25."""
from collections import defaultdict


def main(file_input='input.txt'):
    setup, *states_setup = get_file_contents(file_input).strip().split('\n\n')
    start, steps = parse_setup(setup)
    states = parse_states_setup(states_setup)
    checksum = get_checksum_after(states, start, steps)
    print(f'Checksum after {steps} steps: {checksum}')


def get_checksum_after(states, start, steps):
    """Get checksum value after number of steps, from start state on states."""
    tape = defaultdict(int)
    cursor = 0
    cur_state = start
    for _ in range(steps):
        if_zero, if_one = states[cur_state]
        write_value, move, cur_state = if_zero if tape[cursor] == 0 else if_one
        tape[cursor] = write_value
        cursor += move_cursor(move)
    return sum(tape.values())


def move_cursor(move):
    """Return move value for cursor."""
    return {
        'left': -1,
        'right': 1,
    }[move]


def parse_states_setup(states_setup):
    """Parse states setup to name -> parameters mapping."""
    states = {}
    for setup in states_setup:
        state, params = parse_state_setup(setup)
        states[state] = params
    return states


def parse_state_setup(setup):
    """Parse state setup to name, and tuples with parameters for step."""
    split = [part.split() for part in setup.split('\n')]
    name = split[0][-1][0]
    if_zero = (
        [param[-1][:-1] if param[-1][:-1].isalpha() else int(param[-1][0])
         for param in split[2:5]])
    if_one = (
        [param[-1][:-1] if param[-1][:-1].isalpha() else int(param[-1][0])
         for param in split[6:9]])
    return name, (if_zero, if_one)


def parse_setup(setup):
    """Parse setup lines to starting state and number of steps to process."""
    split = setup.split()
    start = split[3][0]
    steps = int(split[-2])
    return start, steps


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
