"""Advent of Code 2019 Day 16."""


PATTERN_BASE = [0, 1, 0, -1]


def main(file_input='input.txt'):
    input_signal = [
        int(digit) for digit in get_file_contents(file_input)[0].strip()]
    output = phase_signal_n_times(input_signal[:], 100, phase_signal)
    print('First eight digits from the output:',
          ''.join(f'{num}' for num in output[:8]))
    offset = input_signal[:7]
    offset_index = sum(
        digit * 10**(6 - index) for index, digit in enumerate(offset))
    signal = (input_signal[:] * 10_000)[offset_index:]
    output = phase_signal_n_times(signal, 100, part2_phase)
    print('Message embedded in output:',
          ''.join(f'{num}' for num in output[:8]))


def part2_phase(signal):
    """Phase signal single time for the 2nd part."""
    # Based on reddit
    summed = 0
    for index in range(len(signal) - 1, -1, -1):
        summed += signal[index]
        signal[index] = summed % 10
    return signal


def phase_signal_n_times(signal, times, phaser):
    """Phase signal number of times using phaser function."""
    for _ in range(times):
        signal = phaser(signal)
    return signal


def phase_signal(signal):
    """Part 1 phasing function."""
    output = []
    for position, _ in enumerate(signal):
        pattern = create_pattern(PATTERN_BASE, position + 1)
        for _ in range(position):
            next(pattern)
        next_element = sum(
            next(pattern) * element for element in signal[position:])
        last_digit = abs(next_element) % 10
        output.append(last_digit)
    return output


def create_pattern(base, position):
    """Return pattern generated from base and for position."""
    pattern = _pattern(base, position)
    next(pattern)
    while True:
        for element in pattern:
            yield element
        pattern = _pattern(base, position)


def _pattern(base, position):
    """Pattern generator."""
    return (
        element for element in base
        for _ in range(position)
    )


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
