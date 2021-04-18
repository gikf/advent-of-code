"""Advent of Code 2019 Day 12."""
from functools import lru_cache
import re


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    moons = parse_moons(lines)
    after_steps = simulate_steps(moons, 1000)
    total_energy = find_total_energy(after_steps)
    print(f'Total energy after 1000 steps: {total_energy}')
    cycles = simulate_steps(moons)
    *two_cycles, last_cycle = cycles.values()
    steps_to_repeat = int(lcm(lcm(*two_cycles), last_cycle))
    print(f'Steps to reach first repeating state: {steps_to_repeat}')


def simulate_steps(moons, steps=None):
    """Simulate number steps of moons.

    Returns moons after number of steps.
    If steps is None returns cycles of moons."""
    cycles = {}
    initial_moons = moons
    step = 0
    while not steps or step < steps:
        step += 1
        moons = moon_motion(moons)
        if steps:
            continue
        for axis in range(3):
            if axis in cycles:
                continue
            if is_cycle(moons, initial_moons, axis):
                cycles[axis] = step
        if len(cycles) == 3:
            return cycles
    return moons


def is_cycle(moons, initial, axis):
    """Check if moons cycled at the axis to the initial values."""
    for moon, initial in zip(moons, initial):
        if (moon['position'][axis] != initial['position'][axis]
                or moon['velocity'][axis] != initial['velocity'][axis]):
            return False
    return True


def moon_motion(initial_moons):
    """Move moons by one step."""
    moons = []
    for moon in initial_moons:
        cur_velocity = moon['velocity']
        for other_moon in initial_moons:
            if moon == other_moon:
                continue
            velocity_change = join_with_function(
                gravity_effect, moon['position'], other_moon['position'])
            cur_velocity = join_with_function(
                int.__add__, cur_velocity, velocity_change)
        new_position = join_with_function(
            int.__add__, moon['position'], cur_velocity)
        moons.append({
            'position': new_position,
            'velocity': cur_velocity,
        })
    return moons


def join_with_function(func, values1, values2):
    """Join values using func function."""
    return [
        func(value1, value2)
        for value1, value2 in zip(values1, values2)
    ]


def gravity_effect(position, other_position):
    """Return effect other_position has on position."""
    if position == other_position:
        return 0
    elif position > other_position:
        return -1
    return 1


def find_total_energy(moons):
    """Get total energy from moons."""
    return sum(get_energy(moon['position']) * get_energy(moon['velocity'])
               for moon in moons)


def get_energy(values):
    """Get energy from values."""
    return sum(abs(value) for value in values)


def parse_moons(lines):
    """Parse lines to dictionary with positions and velocity."""
    moons = []
    regex = r'([-\d]+)'
    for line in lines:
        position = [int(num) for num in re.findall(regex, line)]
        moons.append({
            'position': position,
            'velocity': [0, 0, 0]
        })
    return moons


@lru_cache()
def lcm(a, b):
    """Least common multiple."""
    return abs(a * b) / gcd(a, b)


@lru_cache()
def gcd(a, b):
    """Greatest common divisor."""
    if b == 0:
        return a
    return gcd(b, a % b)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
