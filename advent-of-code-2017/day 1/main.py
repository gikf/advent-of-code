"""Advent of Code 2017 Day 1."""


def main(file_input='input.txt'):
    captcha = [int(digit)
               for digit in get_file_contents(file_input)[0].strip()]
    for step_size in [1, len(captcha) // 2]:
        matching_digits = get_digits_matching_next(captcha, step_size)
        print(f'Captcha solution for step size {step_size}: '
              f'{sum(matching_digits)}')


def get_digits_matching_next(captcha, step_size=1):
    """Get digits from captcha that are matching next step_size digit."""
    matching_digits = []
    for index, digit in enumerate(captcha):
        next_index = (index + step_size) % len(captcha)
        if digit == captcha[next_index]:
            matching_digits.append(digit)
    return matching_digits


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
