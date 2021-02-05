"""Advent of Code 2016 Day 15."""
import re


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    discs = parse_discs(lines)
    print('Time to press button to get capsule: '
          f'{get_time_to_get_capsule(discs)}')
    discs.append({'#': 7,
                  'positions': 11,
                  'cur_position': 0})
    print('Time to press button to get capsule over seven discs '
          f'{get_time_to_get_capsule(discs)}')


def get_time_to_get_capsule(discs):
    """Get time when discs are aligned to get capsule."""
    time_counter = 0
    while not are_discs_aligned(discs, time_counter):
        time_counter += 1
    return time_counter


def are_discs_aligned(discs, time_counter):
    """Check if all discs are aligned."""
    for align_offset, disc in enumerate(discs, start=1):
        if not is_disc_aligned(disc, time_counter, align_offset):
            return False
    return True


def is_disc_aligned(disc, time_counter, align_offset):
    """Check if disc is aligned."""
    return ((disc['cur_position'] + time_counter + align_offset)
            % disc['positions'] == 0)


def parse_discs(lines):
    """Parse lines to list of dicts."""
    discs = []
    for line in lines:
        discs.append(parse_disc(line))
    return discs


def parse_disc(line):
    """Parse line to dictionary."""
    number, positions, _, cur_position = [
        int(num) for num in re.findall(r'(\d+)', line)]
    return {'#': number,
            'positions': positions,
            'cur_position': cur_position,
            }


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
