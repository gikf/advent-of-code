"""Advent of Code 2019 Day 4."""
from collections import defaultdict


puzzle = '246515-739105'


def main(puzzle=puzzle):
    start, end = [int(num) for num in puzzle.split('-')]
    runs = (
        ('standard requirements', (is_not_decreasing, has_double_digit)),
        ('at least one digit repeated exactly twice',
         (is_not_decreasing, lambda number: has_double_digit(number,
                                                             exact=True))),
    )
    for description, validators in runs:
        passwords_count = count_possible_passwords(
            start, end, validators)
        print(f'Possible passwords with {description}: {passwords_count}')


def count_possible_passwords(start, end, validators):
    """Count possible passwords from start to end, fulfilling validators."""
    count = 0
    for number in range(start, end + 1):
        if all(validator(number) for validator in validators):
            count += 1
    return count


def is_not_decreasing(number):
    """Check if digits in number are not decreasing."""
    digits = get_digits(number)
    return all(
        digits[prev_index] <= digit
        for prev_index, digit in enumerate(digits[1:])
    )


def has_double_digit(number, exact=False):
    """Check if number has double digit.

    If exact is True repeated digit can't be a part of group larger than 2.
    """
    digits = get_digits(number)
    digit_counts = defaultdict(int)
    for digit in digits:
        digit_counts[digit] += 1
    if exact:
        return any(value == 2 for value in digit_counts.values())
    return any(value >= 2 for value in digit_counts.values())


def get_digits(number):
    """Get digits in number from left to right."""
    digits = []
    while number > 0:
        digits.append(number % 10)
        number = number // 10
    return digits[::-1]


if __name__ == '__main__':
    main()
