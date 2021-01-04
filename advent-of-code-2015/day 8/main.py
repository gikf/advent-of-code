"""Advent of Code 2015 Day 8."""
import re


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]

    number_characters_code = count_number_of_characters(
        lines, len)
    number_in_memory = count_number_of_characters(
        lines, count_string_characters)
    print('Number of characters of code for string '
          f'literals: {number_characters_code}')
    print('Number of characters in memory for the '
          f'values of the strings: {number_in_memory}')
    print(f'Difference: {number_characters_code - number_in_memory}')
    number_characters_encoded = count_number_of_characters(
        lines, count_encoded_characters)
    print('Number of characters to represent the '
          f'newly encoded strings: {number_characters_encoded}')
    print(f'Difference: {number_characters_encoded - number_characters_code}')


def count_number_of_characters(strings, representation):
    """Count number of characters in strings, with character representation
    function.
    """
    return sum(representation(string) for string in strings)


def count_encoded_characters(string):
    """Count encoded number of characters.

    "" -> "\"\""
    "abc" -> "\"abc\""
    "aaa\"aaa" -> "\"aaa\\\"aaa\""
    "\x27" -> "\"\\x27\""
    """
    return len(string.replace('\\', '\\\\').replace('"', r'\"')) + 2


def count_string_characters(string):
    """Count number of characters as displayed in string.

    "" -> 0 characters
    "abc" -> 3 characters
    "aaa\"aaa" -> 7 characters
    "\x27" -> 1 character
    """
    string = string[1:-1].replace(r'\\', '_').replace(r'\"', '"')
    regex = r'\\x[0-9a-f]{2}'
    return len(re.sub(regex, '_', string))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
