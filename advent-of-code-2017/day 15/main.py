"""Advent of Code 2017 Day 15."""

puzzle = [699, 124]


def main(puzzle=puzzle):
    matching_pairs = compare_pairs(puzzle, 40_000_000)
    print(f'Final count for 40 million pairs: {matching_pairs}')
    conditions = [lambda num: is_multiply_of(num, 4),
                  lambda num: is_multiply_of(num, 8)]
    matching_pairs = compare_pairs(puzzle, 5_000_000, conditions)
    print('Final count for 5 million pairs with criteria of generated '
          f'numbers to be multiplies of 4 and 8: {matching_pairs}')


def compare_pairs(puzzle, n_times, conditions=None):
    """Compare pairs generated from puzzle values n_times."""
    matching = 0
    value_a, value_b = puzzle
    condition_a, condition_b = conditions or [None, None]
    gen_a = generate(16807, value_a, condition_a)
    gen_b = generate(48271, value_b, condition_b)
    for _ in range(n_times):
        if bin(next(gen_a))[-16:] == bin(next(gen_b))[-16:]:
            matching += 1
    return matching


def is_multiply_of(value, multiply):
    """Check if value is multiply of multiply."""
    return value % multiply == 0


def generate(factor, value, condition=None):
    """Generator of value multiplied by factor, with optional condition."""
    while True:
        value = value * factor % 2147483647
        if condition is not None and not condition(value):
            continue
        yield value


if __name__ == '__main__':
    main()
