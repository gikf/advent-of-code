"""Advent of Code 2015 Day 12."""
import json


def main(file_input='input.txt'):
    data = read_json(file_input)
    counted_numbers = count(data)
    print(f'Sum of all numbers: {counted_numbers}')
    counted_numbers_without_red = count(data, exclude_in_object='red')
    print('Sum of numbers excluding objects having value "red": '
          f'{counted_numbers_without_red}')


def count(data, exclude_in_object=None):
    """Count all numbers in data.

    Optionally exclude from calculation objects including value
    exclude_in_object.
    """
    if isinstance(data, int):
        return data
    elif not data or isinstance(data, str):
        return 0
    summed = 0
    if isinstance(data, dict):
        if exclude_in_object is None or exclude_in_object not in data.values():
            elements = data.values()
        else:
            elements = {}
    elif isinstance(data, list):
        elements = data
    summed += sum(count(element, exclude_in_object) for element in elements)
    return summed


def read_json(file_name):
    """Read json from file."""
    with open(file_name) as f:
        return json.load(f)


if __name__ == '__main__':
    main()
