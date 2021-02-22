"""Advent of Code 2017 Day 7."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    programs, above_to_below = parse_programs(lines)
    bottom = (set(programs) - set(above_to_below)).pop()
    print(f'Bottom program: {bottom}')
    uneven = find_uneven(programs, bottom)
    to_even = weight_for_program_to_even(programs, **uneven)
    print(f"Uneven program: {uneven['program']}, new value to even: {to_even}")


def find_uneven(programs, bottom):
    """Find in programs uneven program."""
    cur_program = programs[bottom]
    if not cur_program['above']:
        return cur_program['weight']
    weights_above = []
    weights = defaultdict(list)
    for above in cur_program['above']:
        result = find_uneven(programs, above)
        if not isinstance(result, int):
            return result
        weights_above.append(result)
        weights[result].append(above)
    if len(set(weights_above)) != 1:
        return extract_uneven_data(weights)
    return cur_program['weight'] + sum(weights_above)


def extract_uneven_data(weights):
    """Return dictionary with information about uneven program."""
    for weight, programs in weights.items():
        if len(programs) != 1:
            needed = weight
        else:
            current = weight
            program = programs[0]
    return {'needed': needed,
            'current': current,
            'program': program}


def weight_for_program_to_even(programs, needed, current, program):
    """Calculate weight of program that would balance all programs."""
    return programs[program]['weight'] + needed - current


def get_weight(programs, program):
    """Get weight of program including above programs."""
    cur_program = programs[program]
    if not cur_program['above']:
        return cur_program['weight']
    weights_above = [get_weight(programs, above)
                     for above in cur_program['above']]
    return cur_program['weight'] + sum(weights_above)


def parse_programs(lines):
    """Parse lines to dictionaries with programs and above_to_below mapping."""
    programs = {}
    above_to_below = {}
    for line in lines:
        name, weight, programs_above = parse_program(line)
        programs[name] = {'weight': weight,
                          'above': programs_above}
        for program in programs_above:
            above_to_below[program] = name
    return programs, above_to_below


def parse_program(line):
    """Parse line to tuple with name, weight and list of programs above."""
    program, *above = line.split(' -> ')
    name, weight = program.split()
    return name, int(weight[1:-1]), above[0].split(', ') if above else []


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
