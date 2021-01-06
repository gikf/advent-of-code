"""Advent of Code 2015 Day 10."""

puzzle = 1113122113


def main(sequence=puzzle):
    sequence_after_40 = apply_process(sequence, 40, look_and_say_sequence)
    print(f'Sequence: {sequence}')
    print(f'Length of sequence after 40 iterations: {len(sequence_after_40)}')
    sequence_after_50 = apply_process(
        sequence_after_40, 10, look_and_say_sequence)
    print(f'Length of sequence after 50 iterations: {len(sequence_after_50)}')


def apply_process(sequence, number_of_times, process):
    """Apply process function to sequence number_of_times."""
    if isinstance(sequence, int):
        sequence = [int(num) for num in str(sequence)]
    for _ in range(number_of_times):
        sequence = process(sequence)
    return sequence


def look_and_say_sequence(sequence):
    """Get next look-and-say of sequence.

    Examples:
    1 -> 11
    11 -> 21
    1211 -> 111221
    111221 -> 312211
    """
    next_sequence = []
    prev_element = None
    count = 1
    for cur_element in sequence:
        if cur_element == prev_element:
            count += 1
        elif prev_element is not None:
            next_sequence.extend((count, prev_element))
            count = 1
        prev_element = cur_element
    next_sequence.extend((count, prev_element))
    return next_sequence


if __name__ == '__main__':
    main()
