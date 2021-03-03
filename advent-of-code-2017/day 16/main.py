"""Advent of Code 2017 Day 16."""


def main(file_input='input.txt'):
    moves = parse_moves(get_file_contents(file_input)[0].strip().split(','))
    after_moves = process_moves(moves, get_programs(16))
    print(f"Order after one dance: {''.join(after_moves)}")
    after_dance = dance(moves, get_programs(16), 1_000_000_000)
    print(f"Order after one billion dances: {''.join(after_dance)}")


def dance(moves, programs, n_times):
    """Perform dance consisting from moves on programs, n_times."""
    counter = 0
    start = ''.join(programs)
    while counter < n_times:
        counter += 1
        programs = process_moves(moves, programs)
        cur_positions = ''.join(programs)
        if start == cur_positions:
            counter = n_times - n_times % counter
            continue
    return programs


def process_moves(moves, programs):
    """Process moves on programs."""
    for move, params in moves:
        func = get_func(move)
        programs = func(programs, params)
    return programs


def spin(programs, steps):
    """Spin programs from the end to the front."""
    return programs[-int(steps):] + programs[:-int(steps)]


def exchange(programs, pair):
    """Swap programs on pair positions in programs."""
    positions = parse_pair(pair)
    swap(programs, positions)
    return programs


def partner(programs, pair):
    """Swap pair of programs in programs."""
    positions = [programs.index(name) for name in parse_pair(pair)]
    swap(programs, positions)
    return programs


def swap(programs, positions):
    """Swap programs in positions."""
    position_a, position_b = positions
    programs[position_a], programs[position_b] = (
        programs[position_b], programs[position_a])


def parse_pair(pair):
    """Parse pair from string to list with two elements."""
    return [int(element) if element.isdigit() else element
            for element in pair.split('/')]


def get_func(move):
    """Map move name to move function."""
    return {
        's': spin,
        'x': exchange,
        'p': partner,
    }[move]


def get_programs(count):
    """Get initially ordered programs."""
    programs = []
    for number in range(count):
        name = chr(ord('a') + number)
        programs.append(name)
    return programs


def parse_moves(moves):
    """Parse moves."""
    parsed = []
    for move in moves:
        parsed.append((move[0], move[1:]))
    return parsed


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
