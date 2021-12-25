"""Advent of Code 2021 Day 3."""


def main(file_input='input.txt'):
    bits = [line.strip() for line in get_file_contents(file_input)]
    counted_bits = count_bits(bits)
    gamma_rate = get_gamma_rate(counted_bits)
    epsilon_rate = reverse_bits(gamma_rate)
    print(f'Gamma rate: {gamma_rate}, epsilon rate: {epsilon_rate}')
    power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
    print(f'Power consumption: {power_consumption}')
    print()

    oxygen_generator_rating = get_rating(counted_bits, bits, oxygen_criteria)
    scrubber_rating = get_rating(counted_bits, bits, scrubber_criteria)
    print(f'Oxygen generator rating: {oxygen_generator_rating}, '
          f'CO2 scrubber rating: {scrubber_rating}')
    life_support = int(oxygen_generator_rating, 2) * int(scrubber_rating, 2)
    print(f'Life support: {life_support}')


def count_bits(bits):
    """Count number of bits on each bit position."""
    counted_bits = {
        position: {'1': 0, '0': 0}
        for position, _ in enumerate(bits[0])
    }
    for line in bits:
        for position, bit in enumerate(line):
            counted_bits[position][bit] += 1
    return counted_bits


def get_rating(counted_bits, bits, criteria):
    """Get from bits rating based on the criteria function."""
    remaining_bits = bits[:]
    for position, _ in enumerate(bits[0]):
        wanted_bit = criteria(counted_bits[position])
        remaining_bits = [
            bit for bit in remaining_bits
            if bit[position] == wanted_bit
        ]
        if len(remaining_bits) == 1:
            return remaining_bits[0]
        counted_bits = count_bits(remaining_bits)
    raise ValueError('No unique bit matching criteria')


def oxygen_criteria(bit_counts):
    """Bit criteria for oxygen generator rating."""
    return '1' if bit_counts['1'] >= bit_counts['0'] else '0'


def scrubber_criteria(bit_counts):
    """Bit criteria for CO2 scrubber rating."""
    return '0' if bit_counts['0'] <= bit_counts['1'] else '1'


def get_gamma_rate(bits):
    """Gamma rate calculations."""
    return ''.join(
        '1' if bits[position]['1'] > bits[position]['0'] else '0'
        for position, _ in enumerate(bits)
    )


def reverse_bits(bits):
    """Reverse bits."""
    bit_to_reverse = {
        '1': '0',
        '0': '1'
    }
    return ''.join(
        bit_to_reverse[bit]
        for bit in bits
    )


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
