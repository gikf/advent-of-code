# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:31:15 2020
"""


def main():
    card_public_key, door_public_key = [
        int(line.strip()) for line in get_file_contents().split('\n')
        if line
    ]
    card_loop_size, door_loop_size = [
        find_loop_size(key)
        for key in (card_public_key, door_public_key)
    ]
    print(f'Loop sizes: {card_loop_size}, {door_loop_size}')
    encryption_key = find_encryption_key(card_loop_size, door_public_key)
    print(f'Encryption key: {encryption_key}')


def find_encryption_key(loop_size, subject_number):
    """Find encryption key from the subject_number and loop_size."""
    value = 1
    for _ in range(loop_size):
        value = transform_value(value, subject_number)
    return value


def transform_value(value, subject_number):
    """Transform value with subject_number."""
    return (value * subject_number) % 20201227


def find_loop_size(key, subject_number=7):
    """Find loop size for given key and subject_number."""
    value = 1
    loops = 0
    while value != key:
        value = transform_value(value, subject_number)
        loops += 1
    return loops


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
