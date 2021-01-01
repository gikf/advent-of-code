"""Advent of Code 2015 Day 5."""


def main(file_input='input.txt'):
    strings = [line.strip() for line in get_file_contents(file_input)]
    nice_strings = get_nice_strings(strings, is_nice_string)
    print(f'Nice strings: {len(nice_strings)}')
    nice_strings_part_two = get_nice_strings(strings, is_nice_string_part_two)
    print(f'Nice strings part two: {len(nice_strings_part_two)}')


def get_nice_strings(strings, check_function):
    """Validate strings with check_function."""
    return [
        string for string in strings
        if check_function(string)
    ]


def is_nice_string(string):
    """Validate niceness of string for part one."""
    return (
        has_three_or_more_vowels(string)
        and has_letters_in_row(string)
        and not has_sub_strings(string, ('ab', 'cd', 'pq', 'xy'))
    )


def is_nice_string_part_two(string):
    """Validate niceness of string for part two."""
    return (has_repeating_pair(string)
            and has_repeating_separated_letter(string))


def has_repeating_pair(string):
    """Check if string has repeating pair of letters."""
    return any(
        string.count(string[index:index+2]) > 1
        for index, _ in enumerate(string[:-1])
    )


def has_repeating_separated_letter(string):
    """Check if string has repeating letter separated by one other letter."""
    return any(
        char == string[index + 2]
        for index, char in enumerate(string[:-2])
    )


def has_three_or_more_vowels(string):
    """Check if string has three or more vowels."""
    return sum(string.count(vowel) for vowel in 'aeiou') >= 3


def has_letters_in_row(string):
    """Check if string has any letter repeating in row."""
    return any(
        char == string[index + 1]
        for index, char in enumerate(string[:-1])
    )


def has_sub_strings(string, sub_strings):
    """Check if string contains any of the sub_strings."""
    return any(
        sub_string in string
        for sub_string in sub_strings
    )


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
